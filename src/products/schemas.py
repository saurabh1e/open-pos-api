from src import ma, BaseSchema
from .models import Brand, Distributor, DistributorBill, Product, Tag, Stock, ProductTax, Tax, Combo, AddOn, Salt


class BrandSchema(BaseSchema):
    class Meta:
        model = Brand
        exclude = ('created_on', 'updated_on')

    name = ma.String()
    retail_shop_id = ma.Integer()


class TagSchema(BaseSchema):
    class Meta:
        model = Tag
        exclude = ('created_on', 'updated_on', 'products')

    name = ma.String()
    retail_shop_id = ma.Integer()


class ProductTaxSchema(BaseSchema):
    class Meta:
        model = ProductTax
        exclude = ('created_on', 'updated_on')
        fields = ('tax_id', 'product_id')

    tax_id = ma.Integer(load=True)
    product_id = ma.Integer(load=True)


class TaxSchema(BaseSchema):
    class Meta:
        model = Tax
        exclude = ('created_on', 'updated_on')
        fields = ('name', 'value', 'id')

    name = ma.String()
    value = ma.Float(precision=2)


class DistributorSchema(BaseSchema):
    class Meta:
        model = Distributor
        exclude = ('created_on', 'updated_on', 'bills', 'products', 'retail_shop')

    name = ma.String()
    phone_numbers = ma.List(ma.Integer())
    emails = ma.List(ma.Email())
    retail_shop_id = ma.Integer()

    bills = ma.Nested('DistributorBillSchema', many=True, exclude=('distributor', 'distributor_id'))


class DistributorBillSchema(BaseSchema):
    class Meta:
        model = DistributorBill
        exclude = ('created_on', 'updated_on')

    purchase_date = ma.Date()
    distributor_id = ma.Integer()

    distributor = ma.Nested('DistributorSchema', many=False)
    purchased_items = ma.Nested('StockSchema', many=True, exclude=('distributor_bill', 'product_variation',
                                                                   'order_items', 'distributor_bill_id'))


class ProductSchema(BaseSchema):
    class Meta:
        model = Product
        exclude = ('created_on', 'updated_on', 'distributor', 'retail_shop', 'brand')

    name = ma.String()
    description = ma.String()
    distributor_id = ma.Integer()
    brand_id = ma.Integer()
    retail_shop_id = ma.Integer()
    mrp = ma.Integer()
    available_stock = ma.Integer()
    brand_name = ma.String(dump_oly=True)
    tags = ma.Nested('TagSchema', many=True)
    salts = ma.Nested('SaltSchema', many=True)
    _links = ma.Hyperlinks(
        {
            'distributor': ma.URLFor('pos.distributor_view', slug='<distributor_id>'),
            'retail_shop': ma.URLFor('pos.retail_shop_view', slug='<retail_shop_id>'),
            'brand': ma.URLFor('pos.brand_view', slug='<brand_id>')
        }
    )

    stocks = ma.Hyperlinks(ma.URLFor('pos.stock_view', __product_id__exact='<id>'))

    taxes = ma.Nested('TaxSchema', many=True)
    available_stocks = ma.Nested('StockSchema', many=True, only=('purchase_amount', 'selling_amount', 'units_purchased',
                                                                 'units_sold', 'expiry_date', 'purchase_date'))


class StockSchema(BaseSchema):
    class Meta:
        model = Stock
        exclude = ('created_on', 'updated_on', 'product', 'order_items')

    purchase_amount = ma.Float(precision=2)
    selling_amount = ma.Float(precision=2)
    units_purchased = ma.Integer()
    batch_number = ma.String()
    expiry_date = ma.Date()
    distributor_bill_id = ma.Integer()
    units_sold = ma.Integer(dump_ony=True)

    # distributor_bill = ma.Nested('DistributorBillSchema', many=False)
    # product = ma.Nested('ProductSchema', many=False)
    # order_items = ma.Nested('OrderItemSchema', many=True)


class SaltSchema(BaseSchema):
    class Meta:
        model = Salt
        exclude = ('created_on', 'updated_on', 'products')


class ComboSchema(BaseSchema):
    class Meta:
        model = Combo
        exclude = ('created_on', 'updated_on', 'products')


class AddOnSchema(BaseSchema):
    class Meta:
        model = AddOn
        exclude = ('created_on', 'updated_on', 'products')

