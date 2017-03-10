from src.utils import ModelResource, operators as ops
from .models import Item, ItemAddOn, Order, OrderDiscount, ItemTax, Status
from .schemas import ItemSchema, ItemTaxSchema, OrderSchema, OrderDiscountSchema, ItemAddOnSchema, StatusSchema


class OrderResource(ModelResource):

    model = Order
    schema = OrderSchema

    optional = ('items', 'time_line')

    order_by = ('id',)

    filters = {
        'id': [ops.Equal],
        'customer_id': [ops.Equal],
        'retail_shop_id': [ops.Equal, ops.In],
        'current_status_id':  [ops.Equal],
    }

    def has_read_permission(self, qs):
        return qs

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):
        return True


class ItemTaxResource(ModelResource):
    model = ItemTax
    schema = ItemTaxSchema

    def has_read_permission(self, qs):
        return qs

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):
        return True


class OrderDiscountResource(ModelResource):
    model = OrderDiscount
    schema = OrderDiscountSchema

    def has_read_permission(self, qs):
        return qs

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):
        return True


class ItemResource(ModelResource):

    model = Item
    schema = ItemSchema

    filters = {

    }

    related_resource = {

    }

    order_by = ['id']

    only = ()

    exclude = ()

    def has_read_permission(self, qs):
        return qs

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):

        return True


class StatusResource(ModelResource):
    model = Status
    schema = StatusSchema

    def has_read_permission(self, qs):
        return qs

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):
        return True


class ItemAddOnResource(ModelResource):
    model = ItemAddOn
    schema = ItemAddOnSchema

    def has_read_permission(self, qs):
        return qs

    def has_change_permission(self, obj):
        return True

    def has_delete_permission(self, obj):
        return True

    def has_add_permission(self, obj):
        return True

