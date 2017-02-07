from src import ma, BaseSchema
from .models import Order, OrderItem, OrderItemTax, OrderDiscount


class OrderSchema(BaseSchema):
    class Meta:
        model = Order

    edit_stock = ma.Boolean()
    sub_total = ma.Float(precision=2)
    total = ma.Float(precision=2)

    customer_id = ma.Integer()
    discount_id = ma.Integer()
    items_count = ma.Integer()

    order_items = ma.Nested('OrderItemSchema', many=True, exclude=('order', 'order_id', 'stock', 'stock_id',
                                                                   'discount_id', 'product_variation_id'))
    customer = ma.Nested('UserSchema', many=False)
    discount = ma.Nested('OrderDiscountSchema', many=False)


class OrderItemSchema(BaseSchema):
    class Meta:
        model = OrderItem

    product_id = ma.Integer(load=True, required=True)
    unit_price = ma.Float(precision=2)
    quantity = ma.Integer()
    order_id = ma.Integer()
    stock_id = ma.Integer()
    discount = ma.Float()
    total_price = ma.Float(dump_only=True)
    discount_amount = ma.Float(dump_only=True)

    product = ma.Nested('ProductSchema', many=False,
                        only=('id', 'name', 'description', 'product', 'product_type'))
    order_item_taxes = ma.Nested('OrderItemTaxSchema', many=True)


class OrderItemTaxSchema(BaseSchema):
    class Meta:
        model = OrderItemTax

    tax_value = ma.Float(precision=2)

    order_item_id = ma.Integer()
    tax_id = ma.Integer()

    tax = ma.Nested('TaxSchema', many=False)
    order_item = ma.Nested('OrderItemSchema', many=False)


class OrderDiscountSchema(BaseSchema):
    class Meta:
        model = OrderDiscount

    name = ma.String()
    amount = ma.Float(precision=2)
