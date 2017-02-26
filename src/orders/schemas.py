from src import ma, BaseSchema
from .models import Order, Item, ItemTax, OrderDiscount, Status, ItemAddOn, Discount


class OrderSchema(BaseSchema):
    class Meta:
        model = Order

    edit_stock = ma.Boolean()
    sub_total = ma.Float(precision=2)
    total = ma.Float(precision=2)

    retail_shop_id = ma.Integer(load=True, required=True)
    customer_id = ma.Integer(load=True, required=False, allow_none=True)
    address_id = ma.Integer(load=True, required=False, partial=True, allow_none=True)
    discount_id = ma.Integer()
    items_count = ma.Integer(dump_only=True)
    amount_due = ma.Integer()

    items = ma.Nested('ItemSchema', many=True, exclude=('order', 'order_id'), load=True)
    retail_shop = ma.Nested('RetailShopSchema', many=False, only=('id', 'name'))
    customer = ma.Nested('CustomerSchema', many=False, dump_only=True, only=['id', 'name', 'mobile_number'])
    address = ma.Nested('AddressSchema', many=False, dump_only=True, only=['id', 'name'])
    discounts = ma.Nested('DiscountSchema', many=True, load=True)


class ItemSchema(BaseSchema):
    class Meta:
        model = Item
        exclude = ('created_on', 'updated_on')

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
                        only=('id', 'name'))
    combo = ma.Nested('ComboSchema', many=False, only=('id', 'name'))
    taxes = ma.Nested('ItemTaxSchema', many=True, exclude=('item',))


class ItemTaxSchema(BaseSchema):
    class Meta:
        model = ItemTax
        exclude = ('created_on', 'updated_on')

    tax_value = ma.Float(precision=2)

    item_id = ma.Integer(load=True)
    tax_id = ma.Integer(load=True)

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
