from sqlalchemy.ext.hybrid import hybrid_property
from flask_security import RoleMixin, UserMixin
from sqlalchemy import UniqueConstraint, func, select, and_

from src.orders.models import Order
from src import db, BaseMixin, ReprMixin


class UserRetailShop(db.Model, BaseMixin):

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    retail_shop_id = db.Column(db.Integer(), db.ForeignKey('retail_shop.id', ondelete='CASCADE'))

    user = db.relationship('User', foreign_keys=[user_id])
    retail_shop = db.relationship('RetailShop', foreign_keys=[retail_shop_id])

    UniqueConstraint(user_id, retail_shop_id)


class RetailShopLocality(db.Model, BaseMixin):

    locality_id = db.Column(db.Integer(), db.ForeignKey('locality.id', ondelete='CASCADE'))
    retail_shop_id = db.Column(db.Integer(), db.ForeignKey('retail_shop.id', ondelete='CASCADE'))

    locality = db.relationship('Locality', foreign_keys=[locality_id])
    retail_shop = db.relationship('RetailShop', foreign_keys=[retail_shop_id])

    UniqueConstraint(locality_id, retail_shop_id)


class CustomerAddress(db.Model, BaseMixin, ReprMixin):

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), index=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), unique=True)

    customer = db.relationship('Customer', foreign_keys=[customer_id])
    address = db.relationship('Address', foreign_keys=[address_id])

    UniqueConstraint(customer_id, address_id)


class RetailBrandAddress(db.Model, BaseMixin, ReprMixin):
    retail_brand_id = db.Column(db.Integer, db.ForeignKey('retail_brand.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

    retail_brand = db.relationship('RetailBrand', foreign_keys=[retail_brand_id])
    address = db.relationship('Address', foreign_keys=[address_id])

    UniqueConstraint(retail_brand_id, address_id)


class RetailBrand(db.Model, BaseMixin, ReprMixin):
    name = db.Column(db.String(80), unique=True)

    retail_shops = db.relationship('RetailShop', back_populates='retail_brand', uselist=True,
                                   cascade='all, delete-orphan')
    addresses = db.relationship('Address', secondary='retail_brand_address')


class RegistrationDetail(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.String(55), nullable=False)
    value = db.Column(db.String(20), nullable=False)

    retail_shop_id = db.Column(db.Integer(), db.ForeignKey('retail_shop.id', ondelete='CASCADE'))
    retail_shop = db.relationship('RetailShop', foreign_keys=[retail_shop_id], back_populates='registration_details')


class RetailShop(db.Model, BaseMixin, ReprMixin):
    name = db.Column(db.String(80), unique=False)
    identity = db.Column(db.String(80), unique=False)

    retail_brand_id = db.Column(db.Integer, db.ForeignKey('retail_brand.id'))
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), unique=True)

    retail_brand = db.relationship('RetailBrand', foreign_keys=[retail_brand_id], back_populates='retail_shops')
    users = db.relationship('User', back_populates='retail_shops', secondary='user_retail_shop', lazy='dynamic')
    products = db.relationship('Product', uselist=True, back_populates='retail_shop')
    orders = db.relationship('Order', uselist=True, back_populates='retail_shop', lazy='dynamic')
    address = db.relationship('Address', foreign_keys=[address_id], uselist=False)
    localities = db.relationship('Locality', secondary='retail_shop_locality')
    registration_details = db.relationship('RegistrationDetail', uselist=True, lazy='dynamic')

    @hybrid_property
    def total_sales(self):
        data = self.orders.with_entities(func.Sum(Order.total), func.Count(Order.id), func.Sum(Order.items_count))\
            .filter(Order.retail_shop_id == self.id).all()[0]

        return {'total_sales': data[0], 'total_orders': data[1], 'total_items': str(data[2])}


class UserRole(db.Model, BaseMixin):

    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

    user = db.relationship('User', foreign_keys=[user_id])
    role = db.relationship('Role', foreign_keys=[role_id])

    UniqueConstraint(user_id, role_id)


class Role(db.Model, BaseMixin, RoleMixin, ReprMixin):
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    users = db.relationship('User', back_populates='roles', secondary='user_role')


class User(db.Model, BaseMixin, UserMixin, ReprMixin):
    email = db.Column(db.String(127), unique=True, nullable=False)
    password = db.Column(db.String(255), default='', nullable=False)
    name = db.Column(db.String(127), nullable=True)
    mobile_number = db.Column(db.String(20), unique=True, nullable=False)

    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())

    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', back_populates='users', secondary='user_role')
    retail_shops = db.relationship('RetailShop', back_populates='users', secondary='user_retail_shop', lazy='dynamic')

    @hybrid_property
    def name(self):
        return '{0}'.format(self.user_profile.first_name) + (' {0}'.format(self.user_profile.last_name)) \
                if self.user_profile.first_name else ''

    @hybrid_property
    def retail_shop_ids(self):
        return [i[0] for i in self.retail_shops.with_entities(RetailShop.id).all()]

    @hybrid_property
    def brand_ids(self):
        return set([i[0] for i in self.retail_shops.with_entities(RetailShop.retail_brand_id).all()])


class PermissionSet(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Customer(db.Model, BaseMixin, ReprMixin):

    email = db.Column(db.String(55), nullable=True)
    name = db.Column(db.String(55), nullable=True)
    active = db.Column(db.Boolean())
    mobile_number = db.Column(db.String(20), nullable=True)
    loyalty_points = db.Column(db.Integer, default=0)
    retail_brand_id = db.Column(db.Integer(), db.ForeignKey('retail_brand.id'))

    retail_brand = db.relationship('RetailBrand', foreign_keys=[retail_brand_id])
    addresses = db.relationship('Address', secondary='customer_address')
    orders = db.relationship('Order', uselist=True, lazy='dynamic')


class Address(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.Text, nullable=False)
    locality_id = db.Column(db.Integer, db.ForeignKey('locality.id'))
    locality = db.relationship('Locality', uselist=False)


class Locality(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.Text, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))

    city = db.relationship('City', uselist=False)

    UniqueConstraint(city_id, name)


class City(db.Model, BaseMixin, ReprMixin):

    name = db.Column(db.Text, nullable=False, unique=True)
