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

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=True)
    retail_shop_id = db.Column(db.Integer, db.ForeignKey('retail_shop.id'), nullable=True)
    current_status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=True)

    order_items = db.relationship('OrderItem', uselist=True, back_populates='order', lazy='dynamic')
    customer = db.relationship('Customer', foreign_keys=[customer_id])
    retail_shop = db.relationship('RetailShop', foreign_keys=[retail_shop_id])
    discounts = db.relationship('Discount', secondary='order_discount')
    current_status = db.relationship('Status', uselist=False, foreign_keys=[current_status_id])
    time_line = db.relationship('Status', secondary='order_status')

    @hybrid_property
    def total_discount(self):
        return sum([discount.value if discount.type == 'VALUE' else float(self.total*discount/100)
                    for discount in self.discounts])

    @hybrid_property
    def total_amount(self):
        return self.total - self.total_discount

    @hybrid_property
    def items_count(self):
        return self.order_items.with_entities(func.Count(OrderItem.id)).scalar()

    @items_count.expression
    def items_count(cls):
        return select([func.Count(OrderItem.id)]).where(OrderItem.order_id == cls.id).as_scalar()


class OrderItem(db.Model, BaseMixin, ReprMixin):

    __repr_fields__ = ['id', 'order_id', 'product_id']

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    unit_price = db.Column(db.Float(precision=2))
    quantity = db.Column(db.SmallInteger)
    discount = db.Column(db.FLOAT(precision=2), default=0, nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=True)

    product = db.relationship('Product', foreign_keys=[product_id])
    order = db.relationship('Order', foreign_keys=[order_id], single_parent=True, back_populates='order_items')
    order_item_taxes = db.relationship('OrderItemTax', uselist=True, cascade='all, delete-orphan',
                                       back_populates='order_item')
    stock = db.relationship('Stock', foreign_keys=[stock_id], single_parent=True, back_populates='order_items')

    @hybrid_property
    def taxes(self):
        return [{'name': i.tax.name, 'amount': i.tax_value*(self.unit_price*self.quantity)/100}
                for i in self.order_item_taxes]

    @hybrid_property
    def total_price(self):
        return float(self.unit_price * self.quantity)

    @hybrid_property
    def discount_amount(self):
        return float((self.total_price*self.discount)/100)


class OrderItemTax(db.Model, BaseMixin):

    tax_value = db.Column(db.Float(precision=2))

    order_item_id = db.Column(db.Integer, db.ForeignKey('order_item.id'))
    tax_id = db.Column(db.Integer, db.ForeignKey('tax.id'))

    tax = db.relationship('Tax', single_parent=True, foreign_keys=[tax_id])
    order_item = db.relationship('OrderItem', single_parent=True, back_populates='order_item_taxes')


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

