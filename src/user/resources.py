from flask_security import current_user
from sqlalchemy import or_, false
from src.utils import ModelResource, operators as ops, AssociationModelResource
from .schemas import User, UserSchema, Role, RoleSchema, UserRole, UserRoleSchema,\
    RetailBrandSchema, RetailShopSchema, UserRetailShopSchema, CustomerSchema, AddressSchema, CitySchema,\
    LocalitySchema, CustomerAddressSchema, CustomerTransactionSchema, PermissionSchema, UserPermissionSchema
from .models import RetailShop, RetailBrand, UserRetailShop, Customer, Locality, City, Address, CustomerAddress,\
    CustomerTransaction, Permission, UserPermission


class UserResource(ModelResource):

    model = User
    schema = UserSchema

    auth_required = True

    roles_accepted = ('admin', 'owner')

    optional = ('retail_shops', 'current_login_at', 'current_login_ip', 'created_on',
                'last_login_at', 'last_login_ip', 'login_count', 'confirmed_at', 'permissions')

    filters = {
        'username': [ops.Equal, ops.Contains],
        'name': [ops.Equal, ops.Contains],
        'active': [ops.Boolean],
        'id': [ops.Equal],
        'retail_brand_id': [ops.Equal, ops.In]
    }

    related_resource = {

    }

    order_by = ['email', 'id', 'name']

    only = ()

    exclude = ()

    def has_read_permission(self, qs):
        if current_user.has_role('admin') or current_user.has_role('admin'):
            return qs.filter(User.retail_brand_id == current_user.retail_brand_id)
        else:
            return qs.filter(User.id == current_user.id)

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):

        return True


class RetailShopResource(ModelResource):
    model = RetailShop
    schema = RetailShopSchema

    optional = ('localities', 'total_sales', 'retail_brand', 'printer_config', 'registration_details')

    filters = {
        'id': [ops.Equal, ops.In]
    }

    auth_required = True
    roles_accepted = ('admin', 'owner')

    def has_read_permission(self, qs):
        return qs

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):
        return True


class RetailBrandResource(ModelResource):
    model = RetailBrand
    schema = RetailBrandSchema

    auth_required = True
    roles_accepted = ('admin', 'owner')

    def has_read_permission(self, qs):
        return qs

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):
        return True


class UserRetailShopResource(AssociationModelResource):

    model = UserRetailShop
    schema = UserRetailShopSchema

    auth_required = True
    roles_accepted = ('admin', 'owner')

    def has_read_permission(self, qs):
        return qs

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):
        return True


class CustomerResource(ModelResource):
    model = Customer
    schema = CustomerSchema

    optional = ('addresses', 'orders', 'retail_brand', 'transactions')

    filters = {
        'name': [ops.Equal, ops.Contains],
        'mobile_number': [ops.Equal, ops.Contains],
        'email': [ops.Equal, ops.Contains],
        'id': [ops.Equal],
        'retail_brand_id': [ops.Equal],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    auth_required = True
    roles_accepted = ('admin', 'owner')

    def has_read_permission(self, qs):
        return qs

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):
        return True


class AddressResource(ModelResource):
    model = Address
    schema = AddressSchema

    auth_required = True
    roles_accepted = ('admin', 'owner')

    def has_read_permission(self, qs):
        return qs

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):
        return True


class LocalityResource(ModelResource):
    model = Locality
    schema = LocalitySchema

    auth_required = True
    roles_accepted = ('admin', 'owner')

    def has_read_permission(self, qs):
        return qs

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):
        return True


class CityResource(ModelResource):
    model = City
    schema = CitySchema

    auth_required = True
    roles_accepted = ('admin', 'owner')

    def has_read_permission(self, qs):
        return qs

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):
        return True


class CustomerAddressResource(AssociationModelResource):

    model = CustomerAddress
    schema = CustomerAddressSchema

    auth_required = True
    roles_accepted = ('admin', 'owner')

    def has_read_permission(self, qs):
        return qs

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):
        return True


class CustomerTransactionResource(ModelResource):

    model = CustomerTransaction
    schema = CustomerTransactionSchema

    auth_required = True
    roles_accepted = ('admin', 'owner')

    def has_read_permission(self, qs):
        return qs

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):
        return True


class PermissionResource(ModelResource):

    model = Permission
    schema = PermissionSchema

    auth_required = True
    roles_accepted = ('admin', 'owner')

    def has_read_permission(self, qs):
        return qs.filter(or_(self.model.is_hidden == False, self.model.is_hidden == None))

    def has_change_permission(self, obj):
        return False

    def has_delete_permission(self, obj):
        return False

    def has_add_permission(self, obj):
        return False


class UserPermissionResource(AssociationModelResource):

    model = UserPermission
    schema = UserPermissionSchema

    auth_required = True
    roles_accepted = ('admin', 'owner')

    def has_read_permission(self, qs):
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.retail_brand_id == User.query.with_entities(User.retail_brand_id)\
            .filter(User.id == obj.user_id).scalar()

    def has_delete_permission(self, obj):
        return current_user.retail_brand_id == User.query.with_entities(User.retail_brand_id) \
            .filter(User.id == obj.user_id).scalar()

    def has_add_permission(self, obj):
        return current_user.retail_brand_id == User.query.with_entities(User.retail_brand_id) \
            .filter(User.id == obj.user_id).scalar()


class RoleResource(ModelResource):
    model = Role
    schema = RoleSchema

    auth_required = True
    roles_accepted = ('admin', 'owner')

    def has_read_permission(self, qs):

        return qs.filter(or_(self.model.is_hidden == False, self.model.is_hidden == None))

    def has_change_permission(self, obj):
        return False

    def has_delete_permission(self, obj):
        return False

    def has_add_permission(self, obj):
        return False


class UserRoleResource(AssociationModelResource):

    model = UserRole
    schema = UserRoleSchema

    auth_required = True
    roles_accepted = ('admin', 'owner')

    def has_read_permission(self, qs):
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.retail_brand_id == User.query.with_entities(User.retail_brand_id) \
            .filter(User.id == obj.user_id).scalar()

    def has_delete_permission(self, obj):
        return current_user.retail_brand_id == User.query.with_entities(User.retail_brand_id) \
            .filter(User.id == obj.user_id).scalar()

    def has_add_permission(self, obj):
        return current_user.retail_brand_id == User.query.with_entities(User.retail_brand_id) \
            .filter(User.id == obj.user_id).scalar()

