from src import BaseView
from .resources import OrderDiscountResource, OrderItemResource, OrderResource, OrderItemTaxResource
from src import api


@api.register()
class OrderView(BaseView):
    resource = OrderResource


@api.register()
class OrderItemView(BaseView):
    resource = OrderItemResource


@api.register()
class OrderDiscountView(BaseView):
    resource = OrderDiscountResource


@api.register()
class OrderItemTaxView(BaseView):
    resource = OrderItemTaxResource
