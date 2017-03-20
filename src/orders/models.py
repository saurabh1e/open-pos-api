from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, select
from src import db, BaseMixin, ReprMixin


class OrderStatus(BaseMixin, db.Model, ReprMixin):
    __repr_fields__ = ['order_id', 'status_id']

    order_id = db.Column(UUID, db.ForeignKey('order.id'), nullable=False, index=True)
    status_id = db.Column(UUID, db.ForeignKey('status.id'), nullable=False, index=True)

    order = db.relationship('Order', foreign_keys=[order_id])
    status = db.relationship('Status', foreign_keys=[status_id])


class Status(BaseMixin, db.Model, ReprMixin):

    name = db.Column(db.String(20), unique=True, nullable=False)
    code = db.Column(db.SmallInteger, unique=True, nullable=False)


class Order(BaseMixin, db.Model, ReprMixin):

    __repr_fields__ = ['id', 'customer_id']

    edit_stock = db.Column(db.Boolean(), default=True)
    sub_total = db.Column(db.Float(precision=2), default=0, nullable=True)
    total = db.Column(db.Float(precision=2), default=0, nullable=True)
    amount_paid = db.Column(db.Float(precision=2), default=0, nullable=True)
    auto_discount = db.Column(db.Float(precision=2), default=0, nullable=True)
    is_void = db.Column(db.Boolean(), default=False)
    invoice_number = db.Column(db.Integer)
    reference_number = db.Column(db.String(12), nullable=True)

    customer_id = db.Column(UUID, db.ForeignKey('customer.id'), nullable=True, index=True)
    user_id = db.Column(UUID, db.ForeignKey('user.id'), nullable=False, index=True)
    address_id = db.Column(UUID, db.ForeignKey('address.id'), nullable=True, index=True)
    retail_shop_id = db.Column(UUID, db.ForeignKey('retail_shop.id'), nullable=False, index=True)
    current_status_id = db.Column(UUID, db.ForeignKey('status.id'), nullable=True, index=True)

    items = db.relationship('Item', uselist=True, back_populates='order', lazy='dynamic', cascade="all, delete-orphan")
    customer = db.relationship('Customer', foreign_keys=[customer_id])
    created_by = db.relationship('User', foreign_keys=[user_id])
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


class Item(BaseMixin, db.Model, ReprMixin):

    __repr_fields__ = ['id', 'order_id', 'product_id']

    unit_price = db.Column(db.Float(precision=2))
    quantity = db.Column(db.Float(precision=2))
    discount = db.Column(db.FLOAT(precision=2), default=0, nullable=False)

    parent_id = db.Column(UUID, db.ForeignKey('item.id'), nullable=True, index=True)
    product_id = db.Column(UUID, db.ForeignKey('product.id'), nullable=True, index=True)
    order_id = db.Column(UUID, db.ForeignKey('order.id'), nullable=True, index=True)
    stock_id = db.Column(UUID, db.ForeignKey('stock.id'), nullable=True, index=True)
    combo_id = db.Column(UUID, db.ForeignKey('combo.id'), nullable=True, index=True)

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

    @hybrid_property
    def retail_shop_id(self):
        return self.order.retail_shop_id

    @retail_shop_id.expression
    def retail_shop_id(self):
        return select([Order.retail_shop_id]).where(Order.id == self.order_id).as_scalar()


class ItemAddOn(BaseMixin, db.Model, ReprMixin):

    item_id = db.Column(UUID, db.ForeignKey('item.id'), index=True)
    add_on_id = db.Column(UUID, db.ForeignKey('add_on.id'), index=True)

    add_on = db.relationship('AddOn', foreign_keys=[add_on_id])
    item = db.relationship('Item', back_populates='add_ons', foreign_keys=[item_id])


class ItemTax(BaseMixin, db.Model):

    tax_value = db.Column(db.Float(precision=2))
    tax_amount = db.Column(db.Float(precision=2))
    item_id = db.Column(UUID, db.ForeignKey('item.id'), index=True)
    tax_id = db.Column(UUID, db.ForeignKey('tax.id'), index=True)

    tax = db.relationship('Tax', foreign_keys=[tax_id])
    item = db.relationship('Item', back_populates='taxes', foreign_keys=[item_id])


class OrderDiscount(BaseMixin, db.Model, ReprMixin):
    __repr_fields__ = ['order_id', 'discount_id']

    order_id = db.Column(UUID, db.ForeignKey('order.id'), nullable=False, index=True)
    discount_id = db.Column(UUID, db.ForeignKey('discount.id'), nullable=False, index=True)

    order = db.relationship('Order', foreign_keys=[order_id])
    discount = db.relationship('Discount', foreign_keys=[discount_id])


class Discount(BaseMixin, db.Model, ReprMixin):

    name = db.Column(db.String(55), nullable=True)
    value = db.Column(db.Float(precision=2), nullable=False)
    type = db.Column(db.Enum('PERCENTAGE', 'FIXED', name='varchar'), nullable=False, default='PERCENTAGE')

    orders = db.relationship('Order', secondary='order_discount')


class Denomination(BaseMixin, db.Model, ReprMixin):

    value = db.Column(db.SmallInteger, default=0)
    name = db.Column(db.String, nullable=False, default='zero')


class OrderDenomination(BaseMixin, db.Model, ReprMixin):

    __repr_fields__ = ['order_id', 'denomination_id']

    order_id = db.Column(UUID, db.ForeignKey('order.id'), nullable=False, index=True)
    denomination_id = db.Column(UUID, db.ForeignKey('denomination.id'), nullable=False, index=True)

    order = db.relationship('Order', foreign_keys=[order_id])
    denomination = db.relationship('Denomination', foreign_keys=[denomination_id])

