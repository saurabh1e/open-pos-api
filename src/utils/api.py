import re
from typing import TypeVar
from abc import abstractproperty

from flask_restful import Api
from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import auth_token_required, roles_accepted, roles_required

from .models import db
from .blue_prints import bp
from .resource import ModelResource
from .exceptions import ResourceNotFound, SQLIntegrityError, SQlOperationalError, CustomException
from .methods import BulkUpdate, List, Fetch, Create, Delete, Update

ModelResourceType = TypeVar('ModelResourceType', bound=ModelResource)


def to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class ApiFactory(Api):
    def init_app(self, app):
        super(ApiFactory, self).init_app(app)

    def register(self, **kwargs):

        def decorator(klass):
            document_name = klass.get_resource().model.__name__.lower()
            name = kwargs.pop('name', document_name)
            url = kwargs.pop('url', '/%s' % to_underscore(klass.get_resource().model.__name__))
            endpoint = to_underscore(klass.__name__)
            view_func = klass.as_view(name)
            methods = klass.api_methods

            for method in methods:
                if method.slug:
                    self.app.add_url_rule(url + '/<string:slug>', endpoint=endpoint, view_func=view_func,
                                          methods=[method.method], **kwargs)
                else:
                    self.app.add_url_rule(url, endpoint=endpoint, view_func=view_func,
                                          methods=[method.method], **kwargs)
            return klass

        return decorator


api = ApiFactory(bp)


class BaseView(Resource):

    api_methods = [BulkUpdate, List, Fetch, Create, Delete, Update]

    def __init__(self):
        if self.get_resource() is not None:
            self.resource = self.get_resource()()
            self.add_method_decorator()

    @classmethod
    @abstractproperty
    def get_resource(cls) -> ModelResourceType:
        pass

    def add_method_decorator(self):
        self.method_decorators = []
        if self.resource.auth_required:
            self.method_decorators.append(roles_required(*[i for i in self.resource.roles_required]))
            self.method_decorators.append(roles_accepted(*[i for i in self.resource.roles_accepted]))
            self.method_decorators.append(auth_token_required)

    def get(self, slug=None):
        if slug:
            obj = self.resource.model.query.get(slug)
            if obj:
                obj = self.resource.has_read_permission(obj)
                return make_response(jsonify(self.resource.schema(exclude=tuple(self.resource.obj_exclude),
                                                                  only=tuple(self.resource.obj_only)).dump(
                    obj, many=False).data), 200)

            return make_response(jsonify({'error': True, 'message': 'Resource not found'}), 404)

        else:
            objects = self.resource.apply_filters(queryset=self.resource.model.query, **request.args)
            objects = self.resource.has_read_permission(objects)

            if '__order_by' in request.args:
                objects = self.resource.apply_ordering(objects, request.args['__order_by'])
            resources = objects.paginate(page=self.resource.page, per_page=self.resource.limit)

            if resources.items:

                return make_response(jsonify({'success': True,
                                              'data': self.resource.schema(exclude=tuple(self.resource.obj_exclude),
                                                                           only=tuple(self.resource.obj_only))
                                             .dump(resources.items, many=True).data, 'total': resources.total}), 200)
            return make_response(jsonify({'error': True, 'Message': 'No Resource Found'}), 404)

    def post(self):
        try:
            data, status = self.resource.save_resource()
        except (SQLIntegrityError, SQlOperationalError) as e:
            db.session.rollback()
            e.message['error'] = True
            return make_response(jsonify(e.message), e.status)
        return make_response(jsonify(data), status)

    def put(self):

        try:
            data, status = self.resource.update_resource()
        except (SQLIntegrityError, SQlOperationalError) as e:
            db.session.rollback()
            e.message['error'] = True
            return make_response(jsonify(e.message), e.status)
        return make_response(jsonify(data), status)

    def patch(self, slug):
        obj = self.resource.model.query.get(slug)
        if not obj:
            return make_response(jsonify({'error': True, 'message': 'Resource not found'}), 404)
        try:
            data, status = self.resource.patch_resource(obj)
        except (SQLIntegrityError, SQlOperationalError) as e:
            db.session.rollback()
            e.message['error'] = True
            return make_response(jsonify(e.message), e.status)
        return make_response(jsonify(data), status)

    def delete(self, slug):

        obj = self.resource.model.query.get(slug)
        if obj:
            if self.resource.has_delete_permission(obj):
                db.session.delete(obj)
                db.session.commit()
                return make_response(jsonify({}), 204)
            else:
                return make_response(
                    jsonify({'error': True, 'Message': 'Forbidden Permission Denied To Delete Resource'}), 403)
        return make_response(jsonify({'error': True, 'message': 'Resource not found'}), 404)


class AssociationView(Resource):

    api_methods = [Update]

    def __init__(self):
        if self.get_resource is not None:
            self.resource = self.get_resource()()
            self.add_method_decorator()

    @abstractproperty
    def get_resource(self) -> ModelResourceType:
        pass

    def add_method_decorator(self):
        self.method_decorators = []
        if self.resource.auth_required:
            self.method_decorators.append(roles_required(*[i for i in self.resource.roles_required]))
            self.method_decorators.append(roles_accepted(*[i for i in self.resource.roles_accepted]))
            self.method_decorators.append(auth_token_required)

    def update(self):

        data = request.json if isinstance(request.json, list) else [request.json]
        for d in data:
            try:
                db.session.begin_nested()
                if d['__action'] == 'add':
                    self.resource.add_relation(request, d)
                if d['__action'] == 'update':
                    self.resource.update_relation(request, d)
                elif d['__action'] == 'remove':
                    self.resource.remove_relation(request, d)
            except (ResourceNotFound, SQLIntegrityError, SQlOperationalError, CustomException) as e:
                db.session.rollback()
                e.message['error'] = True
                return make_response(jsonify(e.message), e.status)
        db.session.commit()

        return make_response(jsonify({'success': True, 'message': 'Updated Successfully', 'data': data}), 200)
