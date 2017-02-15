from .schemas import User, UserSchema, Role, RoleSchema, UserRole, UserRoleSchema,\
    RetailBrandSchema, RetailShopSchema, UserRetailShopSchema, CustomerSchema, AddressSchema, CitySchema, LocalitySchema

from .models import RetailShop, RetailBrand, UserRetailShop, Customer, Locality, City, Address
from src.utils import ModelResource, operators as ops, AssociationModelResource


class RoleResource(ModelResource):
    model = Role
    schema = RoleSchema

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class UserRoleResource(AssociationModelResource):

    model = UserRole
    schema = UserRoleSchema

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class UserResource(ModelResource):

    model = User
    schema = UserSchema

    filters = {
        'username': [ops.Equal, ops.Contains],
        'active': [ops.Boolean],
        'id': [ops.Equal]
    }

    related_resource = {

    }

    order_by = ['email', 'id']

    only = ()

    exclude = ()

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):

        return True


class RetailShopResource(ModelResource):
    model = RetailShop
    schema = RetailShopSchema

    filters = {
        'id': [ops.Equal, ops.In]
    }

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class RetailBrandResource(ModelResource):
    model = RetailBrand
    schema = RetailBrandSchema

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class UserRetailShopResource(AssociationModelResource):

    model = UserRetailShop
    schema = UserRetailShopSchema

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class CustomerResource(ModelResource):
    model = Customer
    schema = CustomerSchema

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class AddressResource(ModelResource):
    model = Address
    schema = AddressSchema

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class LocalityResource(ModelResource):
    model = Locality
    schema = LocalitySchema

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class CityResource(ModelResource):
    model = City
    schema = CitySchema

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True

