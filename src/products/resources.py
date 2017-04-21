from flask_security import current_user
from sqlalchemy.sql import false

from src.utils import ModelResource, AssociationModelResource, operators as ops
from .models import Product, Tax, Stock, Brand, \
    DistributorBill, Distributor, ProductTax, Tag, Combo, AddOn, Salt, ProductDistributor, ProductSalt, \
    ProductTag, BrandDistributor
from .schemas import ProductSchema, TaxSchema, StockSchema, BrandSchema, \
    DistributorBillSchema, DistributorSchema, ProductTaxSchema, TagSchema, ComboSchema, SaltSchema, AddOnSchema, \
    ProductDistributorSchema, ProductSaltSchema, ProductTagSchema, BrandDistributorSchema


class ProductResource(ModelResource):
    model = Product
    schema = ProductSchema

    auth_required = True

    default_limit = 100

    max_limit = 1000

    optional = ('distributors', 'brand', 'retail_shop', 'stocks', 'similar_products', 'available_stocks',
                'last_purchase_amount', 'last_selling_amount', 'stock_required')

    filters = {
        'id': [ops.Equal, ops.In],
        'name': [ops.Equal, ops.Contains],
        'product_name': [ops.Equal, ops.Contains],
        'distributor_name': [ops.Equal, ops.Contains],
        'stock_required': [ops.Equal, ops.Greater, ops.Greaterequal],
        'available_stock': [ops.Equal, ops.Greater, ops.Greaterequal],
        # 'distributor_id': [ops.Equal, ops.In],
        'retail_shop_id': [ops.Equal, ops.In],
        'is_short': [ops.Boolean],
        'is_disabled': [ops.Boolean],
        'created_on': [ops.DateLesserEqual, ops.DateEqual, ops.DateGreaterEqual],
        'updated_on': [ops.Greaterequal, ops.DateGreaterEqual, ops.DateEqual, ops.DateLesserEqual]
    }
    order_by = ['retail_shop_id', 'id', 'name']

    def has_read_permission(self, qs):
        if current_user.has_permission('view_product'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('change_product')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('remove_product')

    def has_add_permission(self, objects):
        if not current_user.has_permission('create_product'):
            return False
        for obj in objects:
            if not current_user.has_shop_access(obj.retail_shop_id):
                return False
        return True


class TagResource(ModelResource):
    model = Tag
    schema = TagSchema

    auth_required = True

    optional = ('products', 'retail_shop')

    order_by = ['retail_shop_id', 'id', 'name']

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    def has_read_permission(self, qs):
        if current_user.has_permission('view_tag'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('change_tag')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('remove_tag')

    def has_add_permission(self, objects):
        if not current_user.has_permission('create_tag'):
            return False
        for obj in objects:
            if not current_user.has_shop_access(obj.retail_shop_id):
                return False
        return True


class StockResource(ModelResource):
    model = Stock
    schema = StockSchema

    auth_required = True

    roles_accepted = ('admin', 'owner', 'staff')

    export = True

    optional = ('product', 'retail_shop', 'distributor_bill', 'product_name', 'retail_shop_id')

    filters = {
        'is_sold': [ops.Boolean],
        'expired': [ops.Boolean],
        'units_available': [ops.Equal, ops.Greater, ops.Greaterequal],
        'units_sold': [ops.Equal, ops.Lesser, ops.LesserEqual],
        'product_name': [ops.Contains, ops.Equal],
        'retail_shop_id': [ops.Equal, ops.In],
        'distributor_id': [ops.Equal, ops.In],
        'distributor_name': [ops.Contains, ops.Equal],
        'updated_on': [ops.DateGreaterEqual, ops.DateEqual, ops.DateLesserEqual],
        'created_on': [ops.DateLesserEqual, ops.DateEqual, ops.DateGreaterEqual]
    }

    order_by = ['expiry_date', 'units_sold', 'created_on']

    only = ()

    exclude = ()

    def has_read_permission(self, qs):
        if current_user.has_permission('view_stock'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('change_stock')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('remove_stock')

    def has_add_permission(self, objects):
        if not current_user.has_permission('create_stock'):
            return False
        for obj in objects:
            if not current_user.has_shop_access(Product.query.with_entities(Product.retail_shop_id)
                                                        .filter(Product.id == obj.product_id).scalar()):
                return False
        return True


class DistributorResource(ModelResource):
    model = Distributor
    schema = DistributorSchema

    auth_required = True

    order_by = ['retail_shop_id', 'id', 'name']

    optional = ('products', 'retail_shop', 'bills')

    filters = {
        'id': [ops.Equal, ops.In],
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    def has_read_permission(self, qs):
        if current_user.has_permission('view_distributor'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('change_distributor')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('remove_distributor')

    def has_add_permission(self, objects):
        if not current_user.has_permission('create_distributor'):
            return False
        for obj in objects:
            if not current_user.has_shop_access(obj.retail_shop_id):
                return False
        return True


class DistributorBillResource(ModelResource):
    model = DistributorBill
    schema = DistributorBillSchema

    auth_required = True

    roles_required = ('admin',)

    optional = ('purchased_items',)

    max_limit = 50

    default_limit = 10

    def has_read_permission(self, qs):
        if current_user.has_permission('view_distributor_bill'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and \
               current_user.has_permission('change_distributor_bill')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and \
               current_user.has_permission('remove_distributor_bill')

    def has_add_permission(self, objects):
        if not current_user.has_permission('create_distributor_bill'):
            return False
        for obj in objects:
            if not current_user.has_shop_access(Distributor.query.with_entities(Distributor.retail_shop_id)
                                                        .filter(Distributor.id == obj.distributor_id).scalar()):
                return False
        return True


class BrandResource(ModelResource):
    model = Brand
    schema = BrandSchema

    auth_required = True

    order_by = ['retail_shop_id', 'id', 'name']

    optional = ('products', 'retail_shop', 'distributors')

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    def has_read_permission(self, qs):
        if current_user.has_permission('view_brand'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('change_brand')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('remove_brand')

    def has_add_permission(self, objects):
        if not current_user.has_permission('create_brand'):
            return False
        for obj in objects:
            if not current_user.has_shop_access(obj.retail_shop_id):
                return False
        return True


class TaxResource(ModelResource):
    model = Tax
    schema = TaxSchema

    auth_required = True
    optional = ('products', 'retail_shop')

    order_by = ['retail_shop_id', 'id', 'name']

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    only = ()

    exclude = ()

    def has_read_permission(self, qs):
        if current_user.has_permission('view_tax'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('change_tax')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('remove_tax')

    def has_add_permission(self, objects):
        if not current_user.has_permission('create_tax'):
            return False
        for obj in objects:
            if not current_user.has_shop_access(obj.retail_shop_id):
                return False
        return True


class SaltResource(ModelResource):
    model = Salt
    schema = SaltSchema

    auth_required = True

    optional = ('products', 'retail_shop')

    order_by = ['retail_shop_id', 'id', 'name']

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    def has_read_permission(self, qs):
        if current_user.has_permission('view_salt'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('change_salt')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('remove_salt')

    def has_add_permission(self, objects):
        if not current_user.has_permission('create_salt'):
            return False
        for obj in objects:
            if not current_user.has_shop_access(obj.retail_shop_id):
                return False
        return True


class AddOnResource(ModelResource):
    model = AddOn
    schema = AddOnSchema

    auth_required = True

    optional = ('products', 'retail_shop')

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    def has_read_permission(self, qs):
        if current_user.has_permission('view_add_on'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('change_add_on')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('remove_add_on')

    def has_add_permission(self, objects):
        if not current_user.has_permission('create_add_on'):
            return False
        for obj in objects:
            if not current_user.has_shop_access(obj.retail_shop_id):
                return False
        return True


class ComboResource(ModelResource):
    model = Combo
    schema = ComboSchema

    auth_required = True

    optional = ('products', 'retail_shop')

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    def has_read_permission(self, qs):
        if current_user.has_permission('view_combo'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('change_combo')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('remove_combo')

    def has_add_permission(self, objects):
        if not current_user.has_permission('create_combo'):
            return False
        for obj in objects:
            if not current_user.has_shop_access(obj.retail_shop_id):
                return False
        return True


class ProductDistributorResource(AssociationModelResource):
    model = ProductDistributor

    schema = ProductDistributorSchema

    auth_required = True

    roles_accepted = ('admin', 'owner')

    def has_read_permission(self, qs):
        if current_user.has_permission('view_product_distributor'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and \
               current_user.has_permission('change_product_distributor')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and \
               current_user.has_permission('remove_product_distributor')

    def has_add_permission(self, obj):
        if not current_user.has_permission('create_product_distributor') or \
                not current_user.has_shop_access(Product.query.with_entities(Product.retail_shop_id)
                                                         .filter(Product.id == obj.product_id).scalar()):
            return False
        return True


class ProductTagResource(AssociationModelResource):
    model = ProductTag

    schema = ProductTagSchema

    auth_required = True

    roles_accepted = ('admin',)

    optional = ('product', 'salt')

    def has_read_permission(self, qs):
        if current_user.has_permission('view_product_tag'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and \
               current_user.has_permission('change_product_tag')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and \
               current_user.has_permission('remove_product_tag')

    def has_add_permission(self, obj):

        if not current_user.has_permission('create_product_tag') or \
                not current_user.has_shop_access(Product.query.with_entities(Product.retail_shop_id)
                                                         .filter(Product.id == obj.product_id).scalar()):
            return False
        return True


class ProductSaltResource(AssociationModelResource):
    model = ProductSalt

    schema = ProductSaltSchema

    auth_required = True

    roles_accepted = ('admin',)

    optional = ('product', 'salt')

    filters = {
        'updated_on': [ops.Greaterequal, ops.DateGreaterEqual, ops.DateEqual, ops.DateLesserEqual],
        'created_on': [ops.Greaterequal, ops.DateGreaterEqual, ops.DateEqual, ops.DateLesserEqual]
    }

    def has_read_permission(self, qs):
        if current_user.has_permission('view_product_salt'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and \
               current_user.has_permission('change_product_salt')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and \
               current_user.has_permission('remove_product_salt')

    def has_add_permission(self, obj):
        if not current_user.has_permission('create_product_salt') or \
                not current_user.has_shop_access(Product.query.with_entities(Product.retail_shop_id)
                                                         .filter(Product.id == obj.product_id).scalar()):
            return False
        return True


class ProductTaxResource(AssociationModelResource):
    model = ProductTax
    schema = ProductTaxSchema

    auth_required = True

    def has_read_permission(self, qs):
        if current_user.has_permission('view_product_tax'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('change_product_tax')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('remove_product_tax')

    def has_add_permission(self, obj):
        if not current_user.has_permission('create_product_tax') or \
                not current_user.has_shop_access(Product.query.with_entities(Product.retail_shop_id)
                                                         .filter(Product.id == obj.product_id).scalar()):
            return False
        return True


class BrandDistributorResource(AssociationModelResource):
    model = BrandDistributor
    schema = BrandDistributorSchema

    optional = ('brand', 'distributor')

    filters = {
        'brand_id': [ops.In, ops.Equal],
        'distributor_id': [ops.In, ops.Equal]
    }

    auth_required = True

    def has_read_permission(self, qs):
        if current_user.has_permission('view_brand_distributor'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission(
            'change_brand_distributor')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission(
            'remove_brand_distributor')

    def has_add_permission(self, obj):
        if not current_user.has_permission('create_brand_distributor') or \
                not current_user.has_shop_access(Product.query.with_entities(Brand.retail_shop_id)
                                                         .filter(Brand.id == obj.brand_id).scalar()):
            return False
        return True
