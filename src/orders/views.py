from src import BaseView
from .resources import OrderDiscountResource, ItemResource, OrderResource, ItemTaxResource, StatusResource,\
    ItemAddOnResource
from src import api


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
