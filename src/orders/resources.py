from sqlalchemy.sql import false
from flask_security import current_user
from src.utils import ModelResource, operators as ops
from .models import Item, ItemAddOn, Order, OrderDiscount, ItemTax, Status
from .schemas import ItemSchema, ItemTaxSchema, OrderSchema, OrderDiscountSchema, ItemAddOnSchema, StatusSchema


class OrderResource(ModelResource):

    model = Order
    schema = OrderSchema

    optional = ('items', 'time_line')

    order_by = ('id', 'invoice_number')

    filters = {
        'id': [ops.Equal],
        'customer_id': [ops.Equal],
        'retail_shop_id': [ops.Equal, ops.In],
        'current_status_id':  [ops.Equal],
    }

    auth_required = True

    def has_read_permission(self, qs):
        if current_user.has_permission('view_order'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        else:
            return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('change_order')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('remove_order')

    def has_add_permission(self, objects):
        if not current_user.has_permission('create_order'):
            return False

        for obj in objects:
            if not current_user.has_shop_access(obj.retail_shop_id):
                return false
        return True


class ItemTaxResource(ModelResource):
    model = ItemTax
    schema = ItemTaxSchema

    auth_required = True
    roles_required = ('admin',)

    def has_read_permission(self, qs):
        if current_user.has_permission('view_order_item'):
            return qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        else:
            return qs.filter(false())

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('change_order_item')

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('remove_order_item')

    def has_add_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id) and current_user.has_permission('create_order_item')


class OrderDiscountResource(ModelResource):
    model = OrderDiscount
    schema = OrderDiscountSchema

    auth_required = True
    roles_required = ('admin',)

    def has_read_permission(self, qs):
        qs = qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id)

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id)

    def has_add_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id)


class ItemResource(ModelResource):

    model = Item
    schema = ItemSchema

    optional = ('add_ons', 'taxes')

    filters = {
        'id': [ops.Equal, ops.In],
        'order_id': [ops.Equal, ops.In],
        'product_id': [ops.Equal, ops.In],
        'retail_shop_id': [ops.Equal, ops.In],
        'stock_id': [ops.Equal, ops.In],
        'update_on': [ops.DateLesserEqual, ops.DateEqual, ops.DateGreaterEqual],
        'created_on': [ops.DateLesserEqual, ops.DateEqual, ops.DateGreaterEqual]
    }

    order_by = ['id']

    only = ()

    exclude = ()

    auth_required = True

    def has_read_permission(self, qs):
        qs = qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id)

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id)

    def has_add_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id)


class StatusResource(ModelResource):
    model = Status
    schema = StatusSchema

    auth_required = True

    roles_required = ('admin',)

    def has_read_permission(self, qs):
        qs = qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id)

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id)

    def has_add_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id)


class ItemAddOnResource(ModelResource):
    model = ItemAddOn
    schema = ItemAddOnSchema

    roles_required = ('admin',)

    auth_required = True

    def has_read_permission(self, qs):
        qs = qs.filter(self.model.retail_shop_id.in_(current_user.retail_shop_ids))
        return qs

    def has_change_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id)

    def has_delete_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id)

    def has_add_permission(self, obj):
        return current_user.has_shop_access(obj.retail_shop_id)

