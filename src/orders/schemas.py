from marshmallow import post_load
from flask_security import current_user
from sqlalchemy import func
from src import ma, BaseSchema
from .models import Order, Item, ItemTax, OrderDiscount, Status, ItemAddOn, Discount


class OrderSchema(BaseSchema):
    class Meta:
        model = Order

    edit_stock = ma.Boolean()
    sub_total = ma.Float(precision=2)
    total = ma.Float(precision=2)

    retail_shop_id = ma.UUID(load=True, required=True)
    reference_number = ma.String(load=True, required=False, partial=True)
    customer_id = ma.UUID(load=True, required=False, allow_none=True)
    address_id = ma.UUID(load=True, required=False, partial=True, allow_none=True)
    discount_id = ma.UUID()
    user_id = ma.UUID(dump_only=True)
    items_count = ma.Integer(dump_only=True)
    amount_due = ma.Integer()
    invoice_number = ma.Integer(dump_only=True)

    items = ma.Nested('ItemSchema', many=True, exclude=('order', 'order_id'), load=True)
    retail_shop = ma.Nested('RetailShopSchema', many=False, only=('id', 'name'))
    customer = ma.Nested('CustomerSchema', many=False, dump_only=True, only=['id', 'name', 'mobile_number'])
    created_by = ma.Nested('UserSchema', many=False, dump_only=True, only=['id', 'name'])
    address = ma.Nested('AddressSchema', many=False, dump_only=True, only=['id', 'name'])
    discounts = ma.Nested('DiscountSchema', many=True, load=True)

    @post_load
    def save_data(self, obj):
        obj.user_id = current_user.id
        obj.invoice_number = Order.query.with_entities(func.Count(Order.id)).filter(Order.retail_shop_id == obj.retail_shop_id).scalar()+1
        return obj


class ItemSchema(BaseSchema):
    class Meta:
        model = Item
        exclude = ('created_on', 'updated_on')

    product_id = ma.UUID(load=True, required=True)
    unit_price = ma.Float(precision=2)
    quantity = ma.Float(precision=2)
    order_id = ma.UUID()
    stock_id = ma.UUID()
    discount = ma.Float()
    discounted_total_price = ma.Float(dump_only=True)
    discounted_unit_price = ma.Float(dump_only=True)
    total_price = ma.Float(dump_only=True)
    discount_amount = ma.Float(dump_only=True)
    children = ma.Nested('self', many=True, default=None, load=True, exclude=('parent',))
    product = ma.Nested('ProductSchema', many=False,
                        only=('id', 'name'))
    combo = ma.Nested('ComboSchema', many=False, only=('id', 'name'))
    taxes = ma.Nested('ItemTaxSchema', many=True, exclude=('item',))
    add_ons = ma.Nested('AddOnSchema', many=True, exclude=('item',))


class ItemTaxSchema(BaseSchema):
    class Meta:
        model = ItemTax
        exclude = ('created_on', 'updated_on')

    tax_value = ma.Float(precision=2)

    item_id = ma.UUID(load=True)
    tax_id = ma.UUID(load=True)

    tax = ma.Nested('TaxSchema', many=False, only=('id', 'name'))
    item = ma.Nested('ItemSchema', many=False)


class OrderDiscountSchema(BaseSchema):
    class Meta:
        model = OrderDiscount
        exclude = ('created_on', 'updated_on')

    name = ma.String()
    amount = ma.Float(precision=2)


class ItemAddOnSchema(BaseSchema):
    class Meta:
        model = ItemAddOn
        exclude = ('created_on', 'updated_on')

    name = ma.String()
    amount = ma.Float(precision=2)


class StatusSchema(BaseSchema):
    class Meta:
        model = Status
        exclude = ('created_on', 'updated_on')

    name = ma.String()
    amount = ma.Float(precision=2)


class DiscountSchema(BaseSchema):
    class Meta:
        model = Discount
        exclude = ('created_on', 'updated_on')

    name = ma.String()
    amount = ma.Float(precision=2)
