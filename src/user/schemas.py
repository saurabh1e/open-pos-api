from src import ma, BaseSchema
from .models import User, Role, Permission, UserRole, RetailShop, RetailBrand, UserRetailShop, \
    Customer, Address, Locality, City, RegistrationDetail, CustomerAddress


class UserSchema(BaseSchema):

    class Meta:
        model = User
        exclude = ('created_on', 'updated_on', 'password', 'current_login_at', 'current_login_ip',
                   'last_login_at', 'last_login_ip', 'login_count', 'confirmed_at')

    id = ma.Integer(dump_only=True)
    email = ma.Email(unique=True, primary_key=True, required=True)
    username = ma.String(required=True)
    name = ma.String(dump_only=True)
    brand_ids = ma.List(ma.Integer)
    retail_shop_ids = ma.List(ma.Integer)
    retail_shops = ma.Nested('RetailShopSchema', many=True)

    _links = ma.Hyperlinks({'shops': ma.URLFor('pos.retail_shop_view', __id__in='<retail_shop_ids>')})
    roles = ma.Nested('RoleSchema', many=True, dump_only=True)


class RoleSchema(BaseSchema):

    class Meta:
        model = Role
        fields = ('name',)

    name = ma.String()


class UserRoleSchema(BaseSchema):

    class Meta:
        model = UserRole
        exclude = ('created_on', 'updated_on')

    id = ma.Integer(load=True)
    user_id = ma.Integer(load=True)
    role_id = ma.Integer(load=True)
    user = ma.Nested('UserSchema', many=False)
    role = ma.Nested('RoleSchema', many=False)


class PermissionSchema(BaseSchema):

    class Meta:
        model = Permission
        exclude = ('users', 'created_on', 'updated_on')


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
    retail_brand_id = ma.Integer()
    retail_brand = ma.Nested('RetailBrandSchema', many=False)
    total_sales = ma.Dict()
    address = ma.Nested('AddressSchema', many=False)
    localities = ma.Nested('LocalitySchema', many=True)
    registration_details = ma.Nested('RegistrationDetailSchema', many=True)


class RetailBrandSchema(BaseSchema):
    class Meta:
        model = RetailBrand
        exclude = ('created_on', 'updated_on')


class UserRetailShopSchema(BaseSchema):
    class Meta:
        model = UserRetailShop
        exclude = ('created_on', 'updated_on')


class CustomerSchema(BaseSchema):
    class Meta:
        model = Customer
        exclude = ('created_on', 'updated_on')

    mobile_number = ma.Integer()
    addresses = ma.Nested('AddressSchema', many=True, load=False, partial=True)


class AddressSchema(BaseSchema):
    class Meta:
        model = Address
        exclude = ('created_on', 'updated_on', 'locality')

    name = ma.String(load=True, required=True)
    locality_id = ma.Integer(load_only=True)
    locality = ma.Nested('LocalitySchema', many=False, load=False, exclude=('city_id',))


class LocalitySchema(BaseSchema):
    class Meta:
        model = Locality
        exclude = ('created_on', 'updated_on')

    city_id = ma.Integer(load=True)
    city = ma.Nested('CitySchema', many=False, load=True)


class CitySchema(BaseSchema):
    class Meta:
        model = City
        exclude = ('created_on', 'updated_on')


class RegistrationDetailSchema(BaseSchema):
    class Meta:
        model = RegistrationDetail
        exclude = ('created_on', 'updated_on', 'retail_shop')


class CustomerAddressSchema(BaseSchema):
    class Meta:
        model = CustomerAddress
        exclude = ('created_on', 'updated_on')

    address_id = ma.Integer(load=True, partial=False)
    customer_id = ma.Integer(load=True, partial=False)
