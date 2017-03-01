from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, select
from src import db, BaseMixin, ReprMixin


class OrderStatus(db.Model, BaseMixin, ReprMixin):
    __repr_fields__ = ['order_id', 'status_id']

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)

    order = db.relationship('Order', foreign_keys=[order_id])
    status = db.relationship('Status', foreign_keys=[status_id])


class Status(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.String(20), unique=True, nullable=False)
    code = db.Column(db.SmallInteger, unique=True, nullable=False)


class Order(db.Model, BaseMixin, ReprMixin):

    __repr_fields__ = ['id', 'customer_id']

    edit_stock = db.Column(db.Boolean(), default=True)
    sub_total = db.Column(db.Float(precision=2), default=0, nullable=True)
    total = db.Column(db.Float(precision=2), default=0, nullable=True)
    amount_paid = db.Column(db.Float(precision=2), default=0, nullable=True)
    auto_discount = db.Column(db.Float(precision=2), default=0, nullable=True)
    is_void = db.Column(db.Boolean(), default=False)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=True)
    retail_shop_id = db.Column(db.Integer, db.ForeignKey('retail_shop.id'), nullable=True)
    current_status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=True)

    items = db.relationship('Item', uselist=True, back_populates='order', lazy='dynamic', cascade="all, delete-orphan")
    customer = db.relationship('Customer', foreign_keys=[customer_id])
    address = db.relationship('Address', foreign_keys=[address_id])
    retail_shop = db.relationship('RetailShop', foreign_keys=[retail_shop_id])
    discounts = db.relationship('Discount', secondary='order_discount', uselist=True)
    denominations = db.relationship('Denomination', secondary='order_denomination', uselist=False)
    current_status = db.relationship('Status', uselist=False, foreign_keys=[current_status_id])
    time_line = db.relationship('Status', secondary='order_status')

    @hybrid_property
    def total_discount(self):
        return sum([discount.value if discount.type == 'VALUE' else float(self.total*discount/100)
                    for discount in self.discounts])

    @hybrid_property
    def items_count(self):
        return self.items.with_entities(func.Count(Item.id)).scalar()

    @items_count.expression
    def items_count(cls):
        return select([func.Count(Item.id)]).where(Item.order_id == cls.id).as_scalar()

    @hybrid_property
    def amount_due(self):
        if self.total and self.amount_paid:
            return self.total - self.amount_paid
        return self.total


class Item(db.Model, BaseMixin, ReprMixin):

    __repr_fields__ = ['id', 'order_id', 'product_id']

    unit_price = db.Column(db.Float(precision=2))
    quantity = db.Column(db.SmallInteger)
    discount = db.Column(db.FLOAT(precision=2), default=0, nullable=False)

    parent_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=True)
    combo_id = db.Column(db.Integer, db.ForeignKey('combo.id'), nullable=True)

    parent = db.relationship('Item', uselist=False, remote_side='Item.id')
    children = db.relationship('Item', remote_side='Item.parent_id')

    product = db.relationship('Product', foreign_keys=[product_id])
    order = db.relationship('Order', foreign_keys=[order_id], single_parent=True, back_populates='items',
                            cascade="all, delete-orphan")
    taxes = db.relationship('ItemTax', uselist=True, cascade='all, delete-orphan',
                            back_populates='item')
    add_ons = db.relationship('ItemAddOn', uselist=True, cascade='all, delete-orphan',
                              back_populates='item')
    stock = db.relationship('Stock', foreign_keys=[stock_id], single_parent=True, back_populates='order_items')

    @hybrid_property
    def total_price(self):
        return float(self.unit_price * self.quantity)

    @hybrid_property
    def discounted_total_price(self):
        return float(self.discounted_unit_price * self.quantity)

    @hybrid_property
    def discounted_unit_price(self):
        return float(self.unit_price-(self.unit_price * self.discount)/100)

    @hybrid_property
    def discount_amount(self):
        return float((self.total_price*self.discount)/100)

    @hybrid_property
    def is_combo(self):
        return self.combo_id is not None


class ItemAddOn(db.Model, BaseMixin, ReprMixin):

    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    add_on_id = db.Column(db.Integer, db.ForeignKey('add_on.id'))

    add_on = db.relationship('AddOn', foreign_keys=[add_on_id])
    item = db.relationship('Item', back_populates='add_ons', foreign_keys=[item_id])


class ItemTax(db.Model, BaseMixin):

    tax_value = db.Column(db.Float(precision=2))
    tax_amount = db.Column(db.Float(precision=2))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    tax_id = db.Column(db.Integer, db.ForeignKey('tax.id'))

    tax = db.relationship('Tax', foreign_keys=[tax_id])
    item = db.relationship('Item', back_populates='taxes', foreign_keys=[item_id])


class OrderDiscount(db.Model, BaseMixin, ReprMixin):
    __repr_fields__ = ['order_id', 'discount_id']

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    discount_id = db.Column(db.Integer, db.ForeignKey('discount.id'), nullable=False)

    order = db.relationship('Order', foreign_keys=[order_id])
    discount = db.relationship('Discount', foreign_keys=[discount_id])


class Discount(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.String(55), nullable=True)
    value = db.Column(db.Float(precision=2), nullable=False)
    type = db.Column(db.Enum('PERCENTAGE', 'FIXED', name='varchar'), nullable=False, default='PERCENTAGE')

    orders = db.relationship('Order', secondary='order_discount')


class Denomination(db.Model, BaseMixin, ReprMixin):

    value = db.Column(db.SmallInteger, default=0)
    name = db.Column(db.String, nullable=False, default='zero')


class OrderDenomination(db.Model, BaseMixin, ReprMixin):

    __repr_fields__ = ['order_id', 'denomination_id']

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    denomination_id = db.Column(db.Integer, db.ForeignKey('denomination.id'), nullable=False)

    order = db.relationship('Order', foreign_keys=[order_id])
    denomination = db.relationship('Denomination', foreign_keys=[denomination_id])

