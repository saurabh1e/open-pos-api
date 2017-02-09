from src.utils import ModelResource
from .models import Item, ItemAddOn, Order, OrderDiscount, ItemTax, Status
from .schemas import ItemSchema, ItemTaxSchema, OrderSchema, OrderDiscountSchema, ItemAddOnSchema, StatusSchema


class OrderResource(ModelResource):

    model = Order
    schema = OrderSchema

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


class ItemTaxResource(ModelResource):
    model = ItemTax
    schema = ItemTaxSchema


class OrderDiscountResource(ModelResource):
    model = OrderDiscount
    schema = OrderDiscountSchema


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

    def has_read_permission(self, request, qs):
        return qs

    def has_change_permission(self, request, obj):
        return True

    def has_delete_permission(self, request, obj):
        return True

    def has_add_permission(self, request, obj):

        return True


class StatusResource(ModelResource):
    model = Status
    schema = StatusSchema


class ItemAddOnResource(ModelResource):
    model = ItemAddOn
    schema = ItemAddOnSchema

