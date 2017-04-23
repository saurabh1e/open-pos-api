from src import ma, BaseSchema
from .models import User, Role, Permission, UserRole, RetailShop, RetailBrand, UserRetailShop, \
    Customer, Address, Locality, City, RegistrationDetail, CustomerAddress, CustomerTransaction, \
    UserPermission, PrinterConfig


class UserSchema(BaseSchema):

    class Meta:
        model = User
        exclude = ('updated_on', 'password')

    id = ma.UUID(dump_only=True)
    email = ma.Email(unique=True, primary_key=True, required=True)
    username = ma.String(required=True)
    name = ma.String(dump_only=True)
    brand_ids = ma.List(ma.UUID)
    retail_shop_ids = ma.List(ma.UUID)
    retail_shops = ma.Nested('RetailShopSchema', many=True)

    _links = ma.Hyperlinks({'shops': ma.URLFor('pos.retail_shop_view', __id__in='<retail_shop_ids>')})
    roles = ma.Nested('RoleSchema', many=True, dump_only=True, only=('id', 'name'))
    permissions = ma.Nested('PermissionSchema', many=True, dump_only=True, only=('id', 'name'))


class RoleSchema(BaseSchema):

    class Meta:
        model = Role
        exclude = ('updated_on', 'created_on', 'users')

    id = ma.UUID()
    name = ma.String()
    permissions = ma.Nested('PermissionSchema', many=True, dump_only=True, only=('id', 'name'))


class UserRoleSchema(BaseSchema):

    class Meta:
        model = UserRole
        exclude = ('created_on', 'updated_on')

    id = ma.UUID(load=True)
    user_id = ma.UUID(load=True)
    role_id = ma.UUID(load=True)
    user = ma.Nested('UserSchema', many=False)
    role = ma.Nested('RoleSchema', many=False)


class PermissionSchema(BaseSchema):

    class Meta:
        model = Permission
        exclude = ('users', 'created_on', 'updated_on')

    role = ma.Nested('RoleSchema', dump_only=True, many=False)


class RetailShopSchema(BaseSchema):

    class Meta:
        model = RetailShop
        exclude = ('created_on', 'updated_on', 'products', 'orders', 'users', 'brands', 'distributors', 'tags', 'taxes')

    _links = ma.Hyperlinks(
        {
            'products': ma.URLFor('pos.product_view', __retail_shop_id__exact='<id>'),
            'brands': ma.URLFor('pos.brand_view', __retail_shop_id__exact='<id>'),
            'distributors': ma.URLFor('pos.distributor_view', __retail_shop_id__exact='<id>'),
            'tags': ma.URLFor('pos.tag_view', __retail_shop_id__exact='<id>'),
            'taxes': ma.URLFor('pos.tax_view', __retail_shop_id__exact='<id>')
        }
    )
    retail_brand_id = ma.UUID()
    retail_brand = ma.Nested('RetailBrandSchema', many=False)
    total_sales = ma.Dict()
    address = ma.Nested('AddressSchema', many=False)
    localities = ma.Nested('LocalitySchema', many=True)
    registration_details = ma.Nested('RegistrationDetailSchema', many=True)
    printer_config = ma.Nested('PrinterConfigSchema', load=True, many=False)


class RetailBrandSchema(BaseSchema):
    class Meta:
        model = RetailBrand
        exclude = ('created_on', 'updated_on')


class UserRetailShopSchema(BaseSchema):
    class Meta:
        model = UserRetailShop
        exclude = ('created_on', 'updated_on')

    user_id = ma.UUID(load=True, allow_none=False)
    retail_shop_id = ma.UUID(load=True, allow_none=False)


class CustomerSchema(BaseSchema):
    class Meta:
        model = Customer
        exclude = ('updated_on',)

    mobile_number = ma.Integer()
    total_orders = ma.Integer(dump_only=True)
    total_billing = ma.Float(precison=2, dump_only=True)
    amount_due = ma.Float(precison=2, dump_only=True)
    addresses = ma.Nested('AddressSchema', many=True, load=False, partial=True)
    retail_brand_id = ma.UUID(load=True)
    retail_shop_id = ma.List(ma.UUID(), load=True)
    retail_brand = ma.Nested('RetailBrandSchema', many=False, only=('id', 'name'))
    transactions = ma.Nested('CustomerTransactionSchema', many=True, only=('id', 'amount', 'created_on'))


class AddressSchema(BaseSchema):
    class Meta:
        model = Address
        exclude = ('created_on', 'updated_on', 'locality')

    name = ma.String(load=True, required=True)
    locality_id = ma.UUID(load_only=True)
    locality = ma.Nested('LocalitySchema', many=False, load=False, exclude=('city_id',))


class LocalitySchema(BaseSchema):
    class Meta:
        model = Locality
        exclude = ('created_on', 'updated_on')

    city_id = ma.UUID(load=True)
    city = ma.Nested('CitySchema', many=False, load=True)


class CitySchema(BaseSchema):
    class Meta:
        model = City
        exclude = ('created_on', 'updated_on')


class RegistrationDetailSchema(BaseSchema):
    class Meta:
        model = RegistrationDetail
        exclude = ('created_on', 'updated_on', 'retail_shop')

    retail_shop_id = ma.UUID(load=True, allow_none=False)


class CustomerAddressSchema(BaseSchema):
    class Meta:
        model = CustomerAddress
        exclude = ('created_on', 'updated_on')

    address_id = ma.UUID(load=True, partial=False)
    customer_id = ma.UUID(load=True, partial=False)


class CustomerTransactionSchema(BaseSchema):
    class Meta:
        model = CustomerTransaction
        exclude = ('updated_on',)

    amount = ma.Float(precision=2, load=True)
    customer_id = ma.UUID(load=True, partial=False, allow_none=False)


class UserPermissionSchema(BaseSchema):
    class Meta:
        model = UserPermission
        exclude = ('created_on', 'updated_on')

    id = ma.UUID(load=True)
    user_id = ma.UUID(load=True)
    permission_id = ma.UUID(load=True)
    user = ma.Nested('UserSchema', many=False)
    permission = ma.Nested('PermissionSchema', many=False)


class PrinterConfigSchema(BaseSchema):

    class Meta:
        model = PrinterConfig
        exclude = ('created_on', 'updated_on')

    retail_shop_id = ma.UUID(load=True, allow_none=False)
    have_bill_printer = ma.Boolean(load=True)
