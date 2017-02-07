from src.utils import ModelResource
from .models import OrderItem, OrderItemTax, Order, OrderDiscount
from .schemas import OrderItemSchema, OrderItemTaxSchema, OrderSchema, OrderDiscountSchema


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


class OrderItemTaxResource(ModelResource):
    model = OrderItemTax
    schema = OrderItemTaxSchema


class OrderDiscountResource(ModelResource):
    model = OrderDiscount
    schema = OrderDiscountSchema


class OrderItemResource(ModelResource):

    model = OrderItem
    schema = OrderItemSchema

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
