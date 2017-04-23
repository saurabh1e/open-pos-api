from src import ma, BaseSchema
from .models import Brand, Distributor, DistributorBill, Product, Tag, Stock, ProductTax, Tax, \
    Combo, AddOn, Salt, ProductSalt, ProductDistributor, ProductTag, BrandDistributor


class BrandSchema(BaseSchema):
    class Meta:
        model = Brand
        exclude = ('created_on', 'updated_on')

    name = ma.String()
    retail_shop_id = ma.UUID()
    retail_shop = ma.Nested('RetailShopSchema', many=False, dump_only=True, only=('id', 'name'))
    distributors = ma.Nested('DistributorSchema', many=True, dump_only=True, only=('id', 'name'))


class TagSchema(BaseSchema):
    class Meta:
        model = Tag
        exclude = ('created_on', 'updated_on')

    id = ma.UUID()
    name = ma.String()
    retail_shop_id = ma.UUID()
    retail_shop = ma.Nested('RetailShopSchema', many=False, dump_only=True, only=('id', 'name'))


class ProductTaxSchema(BaseSchema):
    class Meta:
        model = ProductTax
        exclude = ('created_on', 'updated_on')
        fields = ('tax_id', 'product_id')

    tax_id = ma.UUID(load=True)
    product_id = ma.UUID(load=True)


class TaxSchema(BaseSchema):
    class Meta:
        model = Tax
        exclude = ('created_on', 'updated_on')

    name = ma.String(load=True)
    value = ma.Float(precision=2, load=True)
    retail_shop_id = ma.UUID(load=True)
    retail_shop = ma.Nested('RetailShopSchema', many=False, dump_only=True, only=('id', 'name'))


class DistributorSchema(BaseSchema):
    class Meta:
        model = Distributor
        exclude = ('created_on', 'updated_on')

    id = ma.UUID()
    name = ma.String()
    phone_numbers = ma.List(ma.Integer())
    emails = ma.List(ma.Email())
    retail_shop_id = ma.UUID()
    products = ma.Nested('ProductSchema', many=True, dump_only=True, only=('id', 'name', 'last_selling_amount',
                                                                           'barcode', 'last_purchase_amount',
                                                                           'stock_required', 'quantity_label'))

    retail_shop = ma.Nested('RetailShopSchema', many=False, dump_only=True, only=('id', 'name'))
    bills = ma.Nested('DistributorBillSchema', many=True, exclude=('distributor', 'distributor_id'))


class DistributorBillSchema(BaseSchema):
    class Meta:
        model = DistributorBill
        exclude = ('created_on', 'updated_on')

    purchase_date = ma.Date(load=True)
    distributor_id = ma.UUID(load=True)
    total_items = ma.Integer(dump_only=True)
    bill_amount = ma.Integer(dump_only=True)

    distributor = ma.Nested('DistributorSchema', many=False, only=('id', 'name', 'retail_shop'))
    purchased_items = ma.Nested('StockSchema', many=True, exclude=('distributor_bill', 'order_items', 'product'), load=True)


class ProductSchema(BaseSchema):
    class Meta:
        model = Product
        exclude = ('created_on', 'updated_on')

    name = ma.String()
    description = ma.List(ma.Dict(), allow_none=True)
    sub_description = ma.String(allow_none=True)
    brand_id = ma.UUID()
    retail_shop_id = ma.UUID()
    default_quantity = ma.Float(precision=2, partila=True)
    quantity_label = ma.String(load=True, allow_none=True)
    is_loose = ma.Boolean(load=True, allow_none=True)
    mrp = ma.Integer(dump_only=True)
    available_stock = ma.Integer(dump_only=True)
    barcode = ma.String(max_length=13, min_length=8, load=True, allow_none=False)
    similar_products = ma.List(ma.Integer, dump_only=True)

    last_selling_amount = ma.Float(precision=2, dump_only=True)
    last_purchase_amount = ma.Float(precision=2, dump_only=True)
    stock_required = ma.Integer(dump_only=True)
    is_short = ma.Boolean(dump_only=True)
    distributors = ma.Nested('DistributorSchema', many=True, dump_only=True, only=('id', 'name'))
    brand = ma.Nested('BrandSchema', many=False, dump_only=True, only=('id', 'name'))
    retail_shop = ma.Nested('RetailShopSchema', many=False, dump_only=True, only=('id', 'name'))
    tags = ma.Nested('TagSchema', many=True, only=('id', 'name'), dump_only=True)
    salts = ma.Nested('SaltSchema', many=True, only=('id', 'name'), dump_only=True)

    _links = ma.Hyperlinks(
        {
            'distributor': ma.URLFor('pos.distributor_view', __product_id__exact='<id>'),
            'retail_shop': ma.URLFor('pos.retail_shop_view', slug='<retail_shop_id>'),
            'brand': ma.URLFor('pos.brand_view', slug='<brand_id>'),
            'stocks': ma.URLFor('pos.stock_view', __product_id__exact='<id>')
        }
    )

    stocks = ma.Nested('StockSchema', many=True, only=('purchase_amount', 'selling_amount', 'units_purchased',
                                                       'units_sold', 'expiry_date', 'purchase_date', 'id'))
    taxes = ma.Nested('TaxSchema', many=True, dump_only=True, only=('id', 'name', 'value'))
    available_stocks = ma.Nested('StockSchema', many=True, dump_only=True,
                                 only=('purchase_amount', 'selling_amount', 'units_purchased',
                                       'units_sold', 'expiry_date', 'purchase_date', 'id', 'default_stock'))


class StockSchema(BaseSchema):
    class Meta:
        model = Stock
        exclude = ('order_items', 'created_on', 'updated_on')

    purchase_amount = ma.Float(precision=2)
    selling_amount = ma.Float(precision=2)
    units_purchased = ma.Integer()
    batch_number = ma.String(load=True)
    expiry_date = ma.Date()
    product_name = ma.String()
    product_id = ma.UUID(load=True)
    distributor_bill_id = ma.UUID(allow_none=True)
    units_sold = ma.Integer(dump_only=True, load=False)
    expired = ma.Boolean(dump_only=True)
    quantity_label = ma.String(dump_only=True)
    default_stock = ma.Boolean(load=True, allow_none=True)

    distributor_bill = ma.Nested('DistributorBillSchema', many=False, dump_only=True, only=('id', 'distributor',
                                                                                            'reference_number'))
    product = ma.Nested('ProductSchema', many=False, only=('id', 'name', 'retail_shop'), dump_only=True)


class SaltSchema(BaseSchema):
    class Meta:
        model = Salt
        exclude = ('created_on', 'updated_on')

    retail_shop_id = ma.UUID()
    retail_shop = ma.Nested('RetailShopSchema', many=False, dump_only=True, only=('id', 'name'))


class ComboSchema(BaseSchema):
    class Meta:
        model = Combo
        exclude = ('created_on', 'updated_on')
    retail_shop_id = ma.UUID()


class AddOnSchema(BaseSchema):
    class Meta:
        model = AddOn
        exclude = ('created_on', 'updated_on')
    retail_shop_id = ma.UUID()


class ProductSaltSchema(BaseSchema):

    class Meta:
        model = ProductSalt
        exclude = ('created_on', 'updated_on')

    salt_id = ma.UUID(load=True)
    product_id = ma.UUID(load=True)


class ProductDistributorSchema(BaseSchema):

    class Meta:
        model = ProductDistributor

    distributor_id = ma.UUID(load=True)
    product_id = ma.UUID(load=True)


class ProductTagSchema(BaseSchema):

    class Meta:
        model = ProductTag
        exclude = ('created_on', 'updated_on')

    tag_id = ma.UUID(load=True)
    product_id = ma.UUID(load=True)


class BrandDistributorSchema(BaseSchema):

    class Meta:
        model = BrandDistributor
        exclude = ('created_on', 'updated_on')

    brand_id = ma.UUID(load=True)
    distributor_id = ma.UUID(load=True)
