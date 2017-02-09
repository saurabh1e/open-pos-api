from src import BaseView
from .resources import OrderDiscountResource, ItemResource, OrderResource, ItemTaxResource, StatusResource,\
    ItemAddOnResource
from src import api


@api.register()
class OrderView(BaseView):
    resource = OrderResource


@api.register()
class ItemView(BaseView):
    resource = ItemResource


@api.register()
class OrderDiscountView(BaseView):
    resource = OrderDiscountResource


@api.register()
class ItemTaxView(BaseView):
    resource = ItemTaxResource


@api.register()
class ItemAddOnView(BaseView):
    resource = ItemAddOnResource


@api.register()
class StatusView(BaseView):
    resource = StatusResource
