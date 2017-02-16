from src import BaseView, AssociationView
from .resources import BrandResource, DistributorBillResource, DistributorResource, ProductResource, \
    ProductTaxResource, StockResource, TaxResource, TagResource, ComboResource, AddOnResource, SaltResource
from src import api


@api.register()
class ProductView(BaseView):

    @classmethod
    def get_resource(cls):
        return ProductResource


@api.register()
class TagView(BaseView):

    @classmethod
    def get_resource(cls):
        return TagResource


@api.register()
class StockView(BaseView):

    @classmethod
    def get_resource(cls):
        return StockResource


@api.register()
class DistributorView(BaseView):

    @classmethod
    def get_resource(cls):
        return DistributorResource


@api.register()
class DistributorBillView(BaseView):

    @classmethod
    def get_resource(cls):
        return DistributorBillResource


@api.register()
class TaxView(BaseView):

    @classmethod
    def get_resource(cls):
        return TaxResource


@api.register()
class BrandView(BaseView):

    @classmethod
    def get_resource(cls):
        return BrandResource


@api.register()
class ComboView(BaseView):

    @classmethod
    def get_resource(cls):
        return ComboResource


@api.register()
class AddOnView(BaseView):

    @classmethod
    def get_resource(cls):
        return AddOnResource


@api.register()
class SaltView(BaseView):

    @classmethod
    def get_resource(cls):
        return SaltResource


@api.register()
class ProductTaxAssociationView(AssociationView):

    @classmethod
    def get_resource(cls):
        return ProductTaxResource
