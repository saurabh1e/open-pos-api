from src.utils import ModelResource, AssociationModelResource, operators as ops
from .schemas import ProductSchema, TaxSchema, StockSchema, BrandSchema, \
    DistributorBillSchema, DistributorSchema, ProductTaxSchema, TagSchema, ComboSchema, SaltSchema, AddOnSchema
from .models import Product, Tax, Stock, Brand, \
    DistributorBill, Distributor, ProductTax, ProductType, Tag, Combo, AddOn, Salt


class ProductResource(ModelResource):

    model = Product
    schema = ProductSchema

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
        if not obj.user_id:
            obj.user_id = 1
        return True


class TagResource(ModelResource):
    model = Tag
    schema = TagSchema

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }


class ProductTaxResource(AssociationModelResource):

    model = ProductTax
    schema = ProductTaxSchema


class StockResource(ModelResource):

    model = Stock
    schema = StockSchema

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


class BrandResource(ModelResource):

    model = Brand
    schema = BrandSchema

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }


class TaxResource(ModelResource):

    model = Tax
    schema = TaxSchema

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

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }


class AddOnResource(ModelResource):
    model = AddOn
    schema = AddOnSchema

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }


class ComboResource(ModelResource):
    model = Combo
    schema = ComboSchema

    filters = {
        'name': [ops.Equal, ops.Contains],
        'retail_shop_id': [ops.Equal, ops.In]
    }

