from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import and_, func, select, or_

from src import db, BaseMixin, ReprMixin
from src.orders.models import Item


class Brand(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.String(20), nullable=False)
    retail_shop_id = db.Column(db.Integer, db.ForeignKey('retail_shop.id', ondelete='CASCADE'))

    retail_shop = db.relationship('RetailShop', foreign_keys=[retail_shop_id], uselist=False, backref='brands')
    products = db.relationship('Product', uselist=True, back_populates='brand')


class ProductTax(db.Model, BaseMixin, ReprMixin):

    tax_id = db.Column(db.Integer, db.ForeignKey('tax.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    tax = db.relationship('Tax', foreign_keys=[tax_id])
    product = db.relationship('Product', foreign_keys=[product_id])


class Tax(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.String(15), nullable=False)
    value = db.Column(db.Float(precision=2), nullable=False)

    retail_shop_id = db.Column(db.Integer, db.ForeignKey('retail_shop.id', ondelete='CASCADE'))

    retail_shop = db.relationship('RetailShop', foreign_keys=[retail_shop_id], uselist=False, backref='taxes')
    products = db.relationship('Product', back_populates='taxes', secondary='product_tax', lazy='dynamic')


class Distributor(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.String(127), nullable=False)
    phone_numbers = db.Column(db.ARRAY(item_type='varchar'))
    emails = db.Column(db.ARRAY(item_type='varchar'))

    retail_shop_id = db.Column(db.Integer, db.ForeignKey('retail_shop.id', ondelete='CASCADE'))

    bills = db.relationship('DistributorBill', uselist=True, back_populates='distributor', lazy='dynamic')
    products = db.relationship('Product', uselist=True, back_populates='distributor', lazy='dynamic')
    retail_shop = db.relationship('RetailShop', foreign_keys=[retail_shop_id], uselist=False, backref='distributors')


class DistributorBill(db.Model, BaseMixin, ReprMixin):

    __repr_fields__ = ['id', 'distributor_id']

    purchase_date = db.Column(db.Date, nullable=False)
    distributor_id = db.Column(db.Integer, db.ForeignKey('distributor.id'), nullable=False)

    distributor = db.relationship('Distributor', single_parent=True, back_populates='bills')
    purchased_items = db.relationship('Stock', uselist=True, back_populates='distributor_bill')


class ProductType(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.TEXT())
    retail_shop_id = db.Column(db.Integer, db.ForeignKey('retail_shop.id', ondelete='CASCADE'))


class Tag(db.Model, BaseMixin, ReprMixin):
    name = db.Column(db.String(10), unique=False, nullable=False)
    retail_shop_id = db.Column(db.Integer, db.ForeignKey('retail_shop.id', ondelete='CASCADE'))

    products = db.relationship('Product', back_populates='tags', secondary='product_tag')
    retail_shop = db.relationship('RetailShop', foreign_keys=[retail_shop_id], uselist=False, backref='tags')


class ProductTag(db.Model, BaseMixin, ReprMixin):

    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    tag = db.relationship('Tag', foreign_keys=[tag_id])
    product = db.relationship('Product', foreign_keys=[product_id])


class Product(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.String(20), unique=False, nullable=False)
    min_stock = db.Column(db.SmallInteger, nullable=False)
    auto_discount = db.Column(db.FLOAT(precision=2), default=0, nullable=False)
    description = db.Column(db.JSON, nullable=True)
    sub_description = db.Column(db.Text(), nullable=True)

    retail_shop_id = db.Column(db.Integer, db.ForeignKey('retail_shop.id', ondelete='CASCADE'))
    distributor_id = db.Column(db.Integer, db.ForeignKey('distributor.id'))
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))

    retail_shop = db.relationship('RetailShop', foreign_keys=[retail_shop_id], uselist=False, back_populates='products')
    taxes = db.relationship('Tax', back_populates='products', secondary='product_tax')
    tags = db.relationship('Tag', back_populates='products', secondary='product_tag')
    brand = db.relationship('Brand', foreign_keys=[brand_id], uselist=False, back_populates='products')

    stocks = db.relationship('Stock', uselist=True, cascade="all, delete-orphan", lazy='dynamic')
    distributor = db.relationship('Distributor', back_populates='products')
    combos = db.relationship('Combo', back_populates='products', secondary='combo_product')
    salts = db.relationship('Salt', back_populates='products', secondary='product_salt')
    add_ons = db.relationship('AddOn', back_populates='products', secondary='product_add_on')

    @hybrid_property
    def available_stock(self):
        return self.stocks.filter(or_(Stock.is_sold == False, Stock.is_sold == None))\
            .with_entities(func.Sum(Stock.units_purchased)-func.Sum(Stock.units_sold)).scalar()

    @hybrid_property
    def available_stocks(self):
        return self.stocks.filter(or_(Stock.is_sold == False, Stock.is_sold == None)).all()

    @available_stock.expression
    def available_stock(cls):
        return select([func.Sum(Stock.units_purchased)-func.Sum(Stock.units_sold)])\
            .where(and_(or_(Stock.is_sold == False, Stock.is_sold == None), Stock.product_id == cls.id)).as_scalar()

    @hybrid_property
    def mrp(self):
        mrp = self.stocks.filter(or_(Stock.is_sold == False, Stock.is_sold == None))\
            .with_entities(Stock.selling_amount).order_by(Stock.id).first()
        return mrp[0] if mrp else 0

    @hybrid_property
    def brand_name(self):
        return self.brand.name

    @hybrid_property
    def similar_products(self):
        if len(self.salts):
            return [i[0] for i in Product.query.with_entities(Product.id)
                    .join(ProductSalt, and_(ProductSalt.product_id == Product.id))
                    .filter(ProductSalt.salt_id.in_([i.id for i in self.salts])).group_by(Product.id)
                    .having(func.Count(func.Distinct(ProductSalt.salt_id)) == len(self.salts)).all()]
        return []


class Salt(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.String(127), unique=True, nullable=False)
    retail_shop_id = db.Column(db.Integer, db.ForeignKey('retail_shop.id', ondelete='CASCADE'))

    products = db.relationship('Product', back_populates='salts', secondary='product_salt')
    retail_shop = db.relationship('RetailShop', foreign_keys=[retail_shop_id], uselist=False)


class ProductSalt(db.Model, BaseMixin, ReprMixin):

    __repr_fields__ = ['salt_id', 'product_id']

    salt_id = db.Column(db.Integer, db.ForeignKey('salt.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    salt = db.relationship('Salt', foreign_keys=[salt_id])
    product = db.relationship('Product', foreign_keys=[product_id])


class Stock(db.Model, BaseMixin, ReprMixin):

    __repr_fields__ = ['id', 'product_id']

    purchase_amount = db.Column(db.Float(precision=2))
    selling_amount = db.Column(db.Float(precision=2))
    units_purchased = db.Column(db.SmallInteger, nullable=False)
    batch_number = db.Column(db.String(25), nullable=True)
    expiry_date = db.Column(db.Date, nullable=False)
    purchase_date = db.Column(db.Date, nullable=True, default=db.func.current_timestamp())
    is_sold = db.Column(db.Boolean(), default=False, index=True)

    distributor_bill_id = db.Column(db.Integer, db.ForeignKey('distributor_bill.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, index=True)

    distributor_bill = db.relationship('DistributorBill', single_parent=True, back_populates='purchased_items')
    product = db.relationship('Product', single_parent=True, foreign_keys=product_id)
    order_items = db.relationship('Item', uselist=True, back_populates='stock', lazy='dynamic')

    @hybrid_property
    def units_sold(self):

        total_sold = self.order_items.with_entities(func.Sum(Item.quantity))\
            .filter(Item.stock_id == self.id).scalar()
        if total_sold:
            if total_sold >= self.units_purchased and not self.is_sold:
                self.is_sold = True
                db.session.commit()
            return total_sold
        else:
            return 0

    @units_sold.expression
    def units_sold(cls):
        return select([func.Sum(Item.quantity)]).where(Item.stock_id == cls.id).as_scalar()


class Combo(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.String(55), nullable=False)
    products = db.relationship('Product', back_populates='combos', secondary='combo_product')


class ComboProduct(db.Model, BaseMixin, ReprMixin):

    __repr_fields__ = ['combo_id', 'product_id']

    combo_id = db.Column(db.Integer, db.ForeignKey('combo.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    combo = db.relationship('Combo', foreign_keys=[combo_id])
    product = db.relationship('Product', foreign_keys=[product_id])


class AddOn(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.String(127), unique=True, nullable=False)
    retail_shop_id = db.Column(db.Integer, db.ForeignKey('retail_shop.id', ondelete='CASCADE'))

    products = db.relationship('Product', back_populates='add_ons', secondary='product_add_on')


class ProductAddOn(db.Model, BaseMixin, ReprMixin):

    __repr_fields__ = ['add_on_id', 'product_id']

    add_on_id = db.Column(db.Integer, db.ForeignKey('add_on.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    add_on = db.relationship('AddOn', foreign_keys=[add_on_id])
    product = db.relationship('Product', foreign_keys=[product_id])
