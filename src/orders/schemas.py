from src import ma, BaseSchema
from .models import Order, Item, ItemTax, OrderDiscount, Status, ItemAddOn


class OrderSchema(BaseSchema):
    class Meta:
        model = Order

    edit_stock = ma.Boolean()
    sub_total = ma.Float(precision=2)
    total = ma.Float(precision=2)

    customer_id = ma.Integer()
    discount_id = ma.Integer()
    items_count = ma.Integer()

    items = ma.Nested('OrderItemSchema', many=True, exclude=('order', 'order_id', 'stock', 'stock_id',
                                                             'discount_id', 'product_variation_id'))
    customer = ma.Nested('UserSchema', many=False)
    discount = ma.Nested('OrderDiscountSchema', many=False)


class ItemSchema(BaseSchema):
    class Meta:
        model = Item

    product_id = ma.Integer(load=True, required=True)
    unit_price = ma.Float(precision=2)
    quantity = ma.Integer()
    order_id = ma.Integer()
    stock_id = ma.Integer()
    discount = ma.Float()
    discounted_total_price = ma.Float(dump_only=True)
    discounted_unit_price = ma.Float(dump_only=True)
    total_price = ma.Float(dump_only=True)
    discount_amount = ma.Float(dump_only=True)
    children = ma.Nested('self', many=True, default=None, load=True, exclude=('parent',))
    product = ma.Nested('ProductSchema', many=False,
                        only=('id', 'name', 'sub_description'))
    combo = ma.Nested('ComboSchema', many=False, only=('id', 'name'))
    taxes = ma.Nested('ItemTaxSchema', many=True, exclude=('item',))


class ItemTaxSchema(BaseSchema):
    class Meta:
        model = ItemTax

    tax_value = ma.Float(precision=2)

    item_id = ma.Integer(load=True)
    tax_id = ma.Integer(load=True)

    tax = ma.Nested('TaxSchema', many=False)
    item = ma.Nested('ItemSchema', many=False)


class OrderDiscountSchema(BaseSchema):
    class Meta:
        model = OrderDiscount

    name = ma.String()
    amount = ma.Float(precision=2)


class ItemAddOnSchema(BaseSchema):
    class Meta:
        model = ItemAddOn

    name = ma.String()
    amount = ma.Float(precision=2)


class StatusSchema(BaseSchema):
    class Meta:
        model = Status

    name = ma.String()
    amount = ma.Float(precision=2)

