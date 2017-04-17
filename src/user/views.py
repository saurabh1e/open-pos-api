from flask_restful import Resource
from flask_security.utils import verify_and_update_password, login_user
from flask import request, jsonify, make_response, redirect
from src import BaseView, AssociationView
from src.utils.methods import List
from .resources import UserResource, UserRoleResource, RoleResource,\
    RetailBrandResource, RetailShopResource, UserRetailShopResource, CustomerResource, AddressResource,\
    LocalityResource, CityResource, CustomerAddressResource, CustomerTransactionResource, \
    UserPermissionResource, PermissionResource, PrinterConfigResource, RegistrationDetailResource
from src import api
from .models import User


@api.register()
class UserView(BaseView):

    @classmethod
    def get_resource(cls):
        return UserResource


@api.register()
class RoleView(BaseView):

    api_methods = [List]

    @classmethod
    def get_resource(cls):
        return RoleResource


@api.register()
class PermissionView(BaseView):

    api_methods = [List]

    @classmethod
    def get_resource(cls):
        return PermissionResource


@api.register()
class UserRoleAssociationView(AssociationView):

    @classmethod
    def get_resource(cls):
        return UserRoleResource


@api.register()
class UserPermissionAssociationView(AssociationView):

    @classmethod
    def get_resource(cls):
        return UserPermissionResource


@api.register()
class RetailShopView(BaseView):

    @classmethod
    def get_resource(cls):
        return RetailShopResource


@api.register()
class RetailBrandView(BaseView):

    @classmethod
    def get_resource(cls):
        return RetailBrandResource


@api.register()
class UserRetailShopAssociationView(AssociationView):

    @classmethod
    def get_resource(cls):
        return UserRetailShopResource


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

    @classmethod
    def get_resource(cls):
        return CustomerResource


@api.register()
class AddressView(BaseView):

    @classmethod
    def get_resource(cls):
        return AddressResource


@api.register()
class LocalityView(BaseView):

    @classmethod
    def get_resource(cls):
        return LocalityResource


@api.register()
class CityView(BaseView):

    @classmethod
    def get_resource(cls):
        return CityResource


@api.register()
class CustomerAddressView(AssociationView):

    @classmethod
    def get_resource(cls):
        return CustomerAddressResource


@api.register()
class CustomerTransactionView(BaseView):

    @classmethod
    def get_resource(cls):
        return CustomerTransactionResource


@api.register()
class PrinterConfigView(BaseView):

    @classmethod
    def get_resource(cls):
        return PrinterConfigResource


@api.register()
class RegistrationDetailView(BaseView):

    @classmethod
    def get_resource(cls):
        return RegistrationDetailResource

