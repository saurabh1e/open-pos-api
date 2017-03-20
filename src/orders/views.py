from datetime import datetime
from sqlalchemy import func, and_, cast, Date, DateTime, TIMESTAMP, text, TEXT, Text
from flask import make_response, jsonify, request
from flask_restful import Resource

from src import BaseView, api
from src.user.models import Customer
from src.products.models import Product
from .resources import OrderDiscountResource, ItemResource, OrderResource, ItemTaxResource, StatusResource,\
    ItemAddOnResource
from .models import Order, Item


@api.register()
class OrderView(BaseView):

    @classmethod
    def get_resource(cls):
        return OrderResource


@api.register()
class ItemView(BaseView):

    @classmethod
    def get_resource(cls):
        return ItemResource


@api.register()
class OrderDiscountView(BaseView):

    @classmethod
    def get_resource(cls):
        return OrderDiscountResource


@api.register()
class ItemTaxView(BaseView):

    @classmethod
    def get_resource(cls):
        return ItemTaxResource


@api.register()
class ItemAddOnView(BaseView):

    @classmethod
    def get_resource(cls):
        return ItemAddOnResource


@api.register()
class StatusView(BaseView):

    @classmethod
    def get_resource(cls):
        return StatusResource


class OrderStatResource(Resource):

    def get(self):

        shops = request.args.getlist('__retail_shop_id__in')
        if len(shops) == 1:
            shops = shops[0].split(',')
        from_date = datetime.strptime(request.args['__from'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
        to_date = datetime.strptime(request.args['__to'], '%Y-%m-%dT%H:%M:%S.%fZ').date()

        days = (to_date - from_date).days

        collection_type = 'day'
        if days > 28:
            collection_type = 'week'
            if days > 140:
                collection_type = 'month'

        orders = Order.query.join(Item, and_(Item.order_id == Order.id)).filter(Order.retail_shop_id.in_(shops))

        total_orders, total_sales, total_items, total_quantity, total_due = \
            orders.with_entities(func.Count(Order.id), func.sum(Order.total),
                                 func.Count(func.Distinct(Item.product_id)), func.sum(Item.quantity),
                                 func.Sum(Order.amount_due)).all()[0]

        orders = Order.query.with_entities(func.count(Order.id),
                                           func.cast(func.date_trunc(collection_type,
                                                                     func.cast(Order.created_on, Date)), Text)
                                           .label('dateWeek'))\
            .filter(Order.created_on.between(from_date, to_date))\
            .group_by('dateWeek').all()

        # new_customers = orders.join(Customer, and_(Customer.id == Order.customer_id))\
        #     .with_entities(func.Count(Order.customer_id)).scalar()
        #
        # return_customers = orders.join(Customer, and_(Customer.id == Order.customer_id))\
        #     .with_entities(func.Count(Order.customer_id)).scalar()
        #
        items = Item.query.join(Order, and_(Order.id == Item.order_id))\
            .filter(Order.retail_shop_id.in_(shops))

        max_sold_items = items.join(Product, and_(Product.id == Item.product_id))\
            .with_entities(func.Count(Item.id), Product.name,
                           func.cast(func.date_trunc(collection_type, func.cast(Order.created_on, Date)), Text)
                           .label('dateWeek'))\
            .filter(Order.created_on.between(from_date, to_date))\
            .group_by(Item.product_id, Product.name, 'dateWeek').order_by(-func.Count(Item.id)).limit(10).all()

        # min_sold_items = items.join(Product, and_(Product.id == Item.product_id))\
        #     .with_entities(func.Count(Item.id), Item.product_id,  Product.name)\
        #     .group_by(Item.product_id, Product.name).order_by(func.Count(Item.id)).limit(10).all()

        return make_response(jsonify(dict(total_orders=total_orders, total_sales=total_sales,
                                          total_quantity=total_quantity, max_sold_items=max_sold_items,
                                          total_items=str(total_items), orders=orders)), 200)


api.add_resource(OrderStatResource, '/order_stats/', endpoint='order_stats')
