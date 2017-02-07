from flask_restful import Resource
from flask_security.utils import verify_and_update_password, login_user
from flask import request, jsonify, make_response, redirect
from src import BaseView, AssociationView
from .resources import UserResource, UserRoleResource, RoleResource,\
    RetailBrandResource, RetailShopResource, UserRetailShopResource, CustomerResource, AddressResource,\
    LocalityResource, CityResource
from src import api
from .models import User


@api.register()
class UserView(BaseView):
    resource = UserResource


@api.register()
class RoleView(BaseView):
    resource = RoleResource


@api.register()
class UserRoleAssociationView(AssociationView):

    resource = UserRoleResource


@api.register()
class RetailShopView(BaseView):
    resource = RetailShopResource


@api.register()
class RetailBrandView(BaseView):
    resource = RetailBrandResource


@api.register()
class UserRetailShopAssociationView(AssociationView):

    resource = UserRetailShopResource


class UserLoginResource(Resource):

    model = User

    def post(self):

        if request.json:
            data = request.json

            user = self.model.query.filter(self.model.email == data['email']).first()
            if user and verify_and_update_password(data['password'], user) and login_user(user):

                return jsonify({'id': user.id, 'authentication_token': user.get_auth_token()})
            else:
                return make_response(jsonify({'meta': {'code': 403}}), 403)

        else:
            data = request.form
            user = self.model.query.filter(self.model.email == data['email']).first()
            if user and verify_and_update_password(data['password'], user) and login_user(user):
                return make_response(redirect('/admin/', 302))
            else:
                return make_response(redirect('/api/v1/login', 403))

api.add_resource(UserLoginResource, '/login/', endpoint='login')


@api.register()
class CustomerView(BaseView):
    resource = CustomerResource


@api.register()
class AddressView(BaseView):
    resource = AddressResource


@api.register()
class LocalityView(BaseView):
    resource = LocalityResource


@api.register()
class CityView(BaseView):
    resource = CityResource

