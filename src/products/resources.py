from src.utils import ModelResource, AssociationModelResource, operators as ops
from .schemas import ProductSchema, TaxSchema, StockSchema, BrandSchema, \
    DistributorBillSchema, DistributorSchema, ProductTaxSchema, TagSchema, ComboSchema, SaltSchema, AddOnSchema
from .models import Product, Tax, Stock, Brand, \
    DistributorBill, Distributor, ProductTax, ProductType, Tag, Combo, AddOn, Salt


class ProductResource(ModelResource):

    model = Product
    schema = ProductSchema

    optional = ('distributor', 'brand', 'retail_shop', 'stocks', 'similar_products', 'available_stocks')

    filters = {
        'available_stocks': [ops.Equal, ops.Greater],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class TagResource(ModelResource):
    model = Tag
    schema = TagSchema

    optional = ('products', 'retail_shop')

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class ProductTaxResource(AssociationModelResource):

    model = ProductTax
    schema = ProductTaxSchema

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class StockResource(ModelResource):

    model = Stock
    schema = StockSchema

    optional = ('products', 'retail_shop')

    filters = {
        'units_available': [ops.Equal]
    }

    order_by = ['id']

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


class DistributorResource(ModelResource):

    model = Distributor
    schema = DistributorSchema

    optional = ('products', 'retail_shop')

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class DistributorBillResource(ModelResource):
    model = DistributorBill
    schema = DistributorBillSchema

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class BrandResource(ModelResource):

    model = Brand
    schema = BrandSchema

    optional = ('products', 'retail_shop')

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class TaxResource(ModelResource):

    model = Tax
    schema = TaxSchema
    optional = ('products', 'retail_shop')

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    order_by = ['id']

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


class SaltResource(ModelResource):
    model = Salt
    schema = SaltSchema

    optional = ('products', 'retail_shop')

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class AddOnResource(ModelResource):
    model = AddOn
    schema = AddOnSchema

    optional = ('products', 'retail_shop')

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True


class ComboResource(ModelResource):
    model = Combo
    schema = ComboSchema

    optional = ('products', 'retail_shop')

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):
        return True

