from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.dialects.postgresql import UUID

from flask_security import RoleMixin, UserMixin
from sqlalchemy import UniqueConstraint, func

from src.orders.models import Order
from src import db, BaseMixin, ReprMixin


class UserRetailShop(BaseMixin, db.Model):

    user_id = db.Column(UUID, db.ForeignKey('user.id', ondelete='CASCADE'), index=True, nullable=False)
    retail_shop_id = db.Column(UUID, db.ForeignKey('retail_shop.id', ondelete='CASCADE'), index=True, nullable=False)

    user = db.relationship('User', foreign_keys=[user_id])
    retail_shop = db.relationship('RetailShop', foreign_keys=[retail_shop_id])

    UniqueConstraint(user_id, retail_shop_id)


class RetailShopLocality(BaseMixin, db.Model):

    locality_id = db.Column(UUID, db.ForeignKey('locality.id', ondelete='CASCADE'), index=True)
    retail_shop_id = db.Column(UUID, db.ForeignKey('retail_shop.id', ondelete='CASCADE'), index=True)

    locality = db.relationship('Locality', foreign_keys=[locality_id])
    retail_shop = db.relationship('RetailShop', foreign_keys=[retail_shop_id])

    UniqueConstraint(locality_id, retail_shop_id)


class CustomerAddress(BaseMixin, db.Model, ReprMixin):

    customer_id = db.Column(UUID, db.ForeignKey('customer.id'), index=True)
    address_id = db.Column(UUID, db.ForeignKey('address.id'), unique=True)

    customer = db.relationship('Customer', foreign_keys=[customer_id])
    address = db.relationship('Address', foreign_keys=[address_id])

    UniqueConstraint(customer_id, address_id)


class RetailBrandAddress(BaseMixin, db.Model, ReprMixin):
    retail_brand_id = db.Column(UUID, db.ForeignKey('retail_brand.id'), index=True)
    address_id = db.Column(UUID, db.ForeignKey('address.id'), index=True)

    retail_brand = db.relationship('RetailBrand', foreign_keys=[retail_brand_id])
    address = db.relationship('Address', foreign_keys=[address_id])

    UniqueConstraint(retail_brand_id, address_id)


class RetailBrand(BaseMixin, db.Model, ReprMixin):
    name = db.Column(db.String(80), unique=True)

    retail_shops = db.relationship('RetailShop', back_populates='retail_brand', uselist=True,
                                   cascade='all, delete-orphan')
    users = db.relationship('User', back_populates='retail_brand', uselist=True, cascade='all, delete-orphan')
    addresses = db.relationship('Address', secondary='retail_brand_address')


class RegistrationDetail(BaseMixin, db.Model, ReprMixin):

    name = db.Column(db.String(55), nullable=False)
    value = db.Column(db.String(20), nullable=False)

    retail_shop_id = db.Column(UUID, db.ForeignKey('retail_shop.id', ondelete='CASCADE'), index=True)
    retail_shop = db.relationship('RetailShop', foreign_keys=[retail_shop_id], back_populates='registration_details')


class RetailShop(BaseMixin, db.Model, ReprMixin):
    name = db.Column(db.String(80), unique=False)
    identity = db.Column(db.String(80), unique=False)

    retail_brand_id = db.Column(UUID, db.ForeignKey('retail_brand.id'), index=True)
    address_id = db.Column(UUID, db.ForeignKey('address.id'), unique=True, index=True)
    invoice_number = db.Column(db.Integer, default=0, nullable=False)
    separate_offline_billing = db.Column(db.Boolean, default=False)

    retail_brand = db.relationship('RetailBrand', foreign_keys=[retail_brand_id], back_populates='retail_shops')
    users = db.relationship('User', back_populates='retail_shops', secondary='user_retail_shop', lazy='dynamic')
    products = db.relationship('Product', uselist=True, back_populates='retail_shop')
    orders = db.relationship('Order', uselist=True, back_populates='retail_shop', lazy='dynamic')
    address = db.relationship('Address', foreign_keys=[address_id], uselist=False)
    localities = db.relationship('Locality', secondary='retail_shop_locality')
    registration_details = db.relationship('RegistrationDetail', uselist=True, lazy='dynamic')
    printer_config = db.relationship('PrinterConfig', uselist=False)

    @hybrid_property
    def total_sales(self):
        data = self.orders.with_entities(func.Sum(Order.total), func.Count(Order.id), func.Sum(Order.items_count))\
            .filter(Order.retail_shop_id == self.id).all()[0]

        return {'total_sales': data[0], 'total_orders': data[1], 'total_items': str(data[2])}


class UserRole(BaseMixin, db.Model):

    user_id = db.Column(UUID, db.ForeignKey('user.id', ondelete='CASCADE'), index=True)
    role_id = db.Column(UUID, db.ForeignKey('role.id', ondelete='CASCADE'), index=True)

    user = db.relationship('User', foreign_keys=[user_id])
    role = db.relationship('Role', foreign_keys=[role_id])

    UniqueConstraint(user_id, role_id)


class UserPermission(BaseMixin, db.Model):

    user_id = db.Column(UUID, db.ForeignKey('user.id', ondelete='CASCADE'), index=True)
    permission_id = db.Column(UUID, db.ForeignKey('permission.id', ondelete='CASCADE'), index=True)

    user = db.relationship('User', foreign_keys=[user_id])
    permission = db.relationship('Permission', foreign_keys=[permission_id])

    UniqueConstraint(user_id, permission_id)


class Role(BaseMixin, db.Model, RoleMixin, ReprMixin):
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    is_hidden = db.Column(db.Boolean(), default=False)

    permissions = db.relationship('Permission', uselist=True, lazy='dynamic', back_populates='role')
    users = db.relationship('User', back_populates='roles', secondary='user_role')


class User(BaseMixin, db.Model, UserMixin, ReprMixin):
    email = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(255), default='', nullable=False)
    name = db.Column(db.String(55), nullable=False)
    mobile_number = db.Column(db.String(20), unique=True, nullable=False)

    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())

    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)

    retail_brand_id = db.Column(UUID, db.ForeignKey('retail_brand.id'), index=True)

    retail_brand = db.relationship('RetailBrand', foreign_keys=[retail_brand_id], back_populates='users')
    roles = db.relationship('Role', back_populates='users', secondary='user_role')
    permissions = db.relationship('Permission', back_populates='users', secondary='user_permission', lazy='dynamic')
    retail_shops = db.relationship('RetailShop', back_populates='users', secondary='user_retail_shop', lazy='dynamic')

    @hybrid_property
    def retail_shop_ids(self):
        return [i[0] for i in self.retail_shops.with_entities(RetailShop.id).all()]

    @retail_shop_ids.expression
    def retail_shop_ids(self):
        from sqlalchemy import select
        return select([UserRetailShop.retail_shop_id]).where(UserRetailShop.user_id == self.id).label('retail_shop_ids').limit(1)

    @hybrid_method
    def has_shop_access(self, shop_id):
        return db.session.query(UserRetailShop.query.filter(UserRetailShop.retail_shop_id == shop_id,
                                                            UserRetailShop.user_id == self.id).exists()).scalar()

    @hybrid_method
    def has_permission(self, permission):
        return db.session.query(self.permissions.filter(Permission.name == permission).exists()).scalar()

    @hybrid_property
    def is_owner(self):
        return self.has_role('owner')


class Permission(BaseMixin, db.Model, ReprMixin):

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    type = db.Column(db.String(15), nullable=True)
    is_hidden = db.Column(db.Boolean(), default=False)
    role_id = db.Column(UUID, db.ForeignKey('role.id'), nullable=True)

    role = db.relationship('Role', back_populates='permissions', uselist=False)
    users = db.relationship('User', back_populates='permissions', secondary='user_permission')


class Customer(BaseMixin, db.Model, ReprMixin):

    email = db.Column(db.String(55), nullable=True)
    name = db.Column(db.String(55), nullable=True)
    active = db.Column(db.Boolean())
    mobile_number = db.Column(db.String(20), nullable=True)
    loyalty_points = db.Column(db.Integer, default=0)
    retail_brand_id = db.Column(UUID, db.ForeignKey('retail_brand.id'), index=True)

    retail_brand = db.relationship('RetailBrand', foreign_keys=[retail_brand_id])
    addresses = db.relationship('Address', secondary='customer_address')
    orders = db.relationship('Order', uselist=True, lazy='dynamic')
    transactions = db.relationship('CustomerTransaction', uselist=True, lazy='dynamic')

    @hybrid_property
    def total_orders(self):
        return self.orders.with_entities(func.coalesce(func.Count(Order.id), 0)).scalar()

    @hybrid_property
    def total_billing(self):
        return self.orders.with_entities(func.coalesce(func.Sum(Order.total), 0)).scalar()

    @hybrid_property
    def amount_due(self):
        return self.orders.with_entities(func.coalesce(func.Sum(Order.total), 0) -
                                         func.coalesce(func.Sum(Order.amount_paid), 0)).scalar() - \
               self.transactions.with_entities(func.coalesce(func.Sum(CustomerTransaction.amount), 0)).scalar()


class CustomerTransaction(BaseMixin, db.Model, ReprMixin):

    amount = db.Column(db.Float(precision=2), nullable=False, default=0)
    customer_id = db.Column(UUID, db.ForeignKey('customer.id'), nullable=False, index=True)
    customer = db.relationship('Customer', foreign_keys=[customer_id])


class Address(BaseMixin, db.Model, ReprMixin):

    name = db.Column(db.Text, nullable=False)
    locality_id = db.Column(UUID, db.ForeignKey('locality.id'), index=True)
    locality = db.relationship('Locality', uselist=False)


class Locality(BaseMixin, db.Model, ReprMixin):

    name = db.Column(db.Text, nullable=False)
    city_id = db.Column(UUID, db.ForeignKey('city.id'), index=True)

    city = db.relationship('City', uselist=False)

    UniqueConstraint(city_id, name)


class City(BaseMixin, db.Model, ReprMixin):

    name = db.Column(db.Text, nullable=False, unique=True)


class PrinterConfig(BaseMixin, db.Model, ReprMixin):

    header = db.Column(db.Text, nullable=True)
    footer = db.Column(db.Text, nullable=True)

    bill_template = db.Column(db.Text, nullable=True)
    receipt_template = db.Column(db.Text, nullable=True)

    bill_printer_type = db.Column(db.Enum('thermal', 'dot_matrix', 'laser', name='varchar'))
    receipt_printer_type = db.Column(db.Enum('thermal', 'dot_matrix', 'laser', name='varchar'))
    label_printer_type = db.Column(db.Enum('1x1', '2x1', '3x1', '4x1', name='varchar'))

    have_receipt_printer = db.Column(db.Boolean(), default=False)
    have_bill_printer = db.Column(db.Boolean(), default=False)

    retail_shop_id = db.Column(UUID, db.ForeignKey('retail_shop.id'))

