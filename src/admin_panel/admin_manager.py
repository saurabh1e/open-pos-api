from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin_impexp.admin_impexp import AdminImportExport
from flask_security import current_user
from src import admin, db
from src.user.models import User, Role, Permission, UserRole, RetailBrand, RetailShop, UserRetailShop, \
    Address, Locality, City, Customer, RegistrationDetail, CustomerAddress, CustomerTransaction, PrinterConfig
from src.orders.models import OrderDiscount, Status, Item, ItemAddOn, Order, Discount, ItemTax, OrderStatus
from src.products.models import ProductTax, Tax, Product, ProductType, Stock, Distributor,\
    DistributorBill, Tag, Brand, Salt, AddOn, Combo, ProductSalt, BrandDistributor, ProductTag


class MyModel(AdminImportExport):
    page_size = 100
    can_set_page_size = True
    can_view_details = True

    def is_accessible(self):
        return current_user.has_role('admin')


class RetailShopAdmin(MyModel):

    column_filters = ('name', 'products.name')
    form_excluded_columns = ('products', 'brands', 'orders')

    form_ajax_refs = {
        'registration_details': QueryAjaxModelLoader('registration_details', db.session, RegistrationDetail,
                                                     fields=['name'], page_size=10),
        'printer_config': QueryAjaxModelLoader('printer_config', db.session, PrinterConfig, fields=['id'], page_size=10),
        'users': QueryAjaxModelLoader('users', db.session, User, fields=['name'], page_size=10),
        'orders': QueryAjaxModelLoader('orders', db.session, Order, fields=['id'], page_size=10),
        'retail_brand': QueryAjaxModelLoader('retail_brand', db.session, RetailBrand, fields=['name'], page_size=10),
        'brands': QueryAjaxModelLoader('brands', db.session, Brand, fields=['name'], page_size=10),
        'tags': QueryAjaxModelLoader('tags', db.session, Tag, fields=['name'], page_size=10),
        'salts': QueryAjaxModelLoader('salts', db.session, Salt, fields=['name'], page_size=10),
        'taxes': QueryAjaxModelLoader('taxes', db.session, Tax, fields=['name'], page_size=10),
        'products': QueryAjaxModelLoader('products', db.session, Product, fields=['name'], page_size=10),
        'distributors': QueryAjaxModelLoader('distributors', db.session, Distributor, fields=['name'], page_size=10),

    }


class DistributorBillAdmin(MyModel):

    column_searchable_list = ('id',  'purchase_date', 'reference_number')
    column_filters = ('distributor.name', 'distributor.retail_shop.name', 'purchase_date', 'reference_number')

    form_ajax_refs = {
        'distributor': QueryAjaxModelLoader('distributor', db.session, Distributor, fields=['name'], page_size=10),
        'purchased_items':  QueryAjaxModelLoader('purchased_items', db.session, Stock, fields=['product_name'],
                                                 page_size=10),
    }


class ProductAdmin(MyModel):

    column_filters = ('retail_shop', 'brand', 'tags', 'taxes', 'salts')

    column_searchable_list = ('id', 'retail_shop_id', 'name', 'quantity_label')
    column_editable_list = ('retail_shop_id', 'name', 'quantity_label', 'default_quantity', 'sub_description',
                            'is_loose', 'is_disabled', 'barcode', 'min_stock', 'auto_discount')

    form_ajax_refs = {
        'brand': QueryAjaxModelLoader('brand', db.session, Brand, fields=['name'], page_size=10),
        'retail_shop': QueryAjaxModelLoader('retail_shop', db.session, RetailShop, fields=['name'], page_size=10),
        'stocks': QueryAjaxModelLoader('stocks', db.session, Stock, fields=['product_name'], page_size=10),
        'tags': QueryAjaxModelLoader('tags', db.session, Tag, fields=['name'], page_size=10),
        'salts': QueryAjaxModelLoader('salts', db.session, Salt, fields=['name'], page_size=10),
        'taxes': QueryAjaxModelLoader('taxes', db.session, Tax, fields=['name'], page_size=10),
    }

    inline_models = (Tag, Tax, Salt)


class DistributorAdmin(MyModel):

    column_editable_list = ('name',)
    column_filters = ('brands', 'retail_shop')
    form_ajax_refs = {
        'brands': QueryAjaxModelLoader('brands', db.session, Brand, fields=['name'], page_size=10),
    }


class TaxAdmin(MyModel):

    column_sortable_list = ('name',)
    column_searchable_list = ('id', 'retail_shop_id', 'name')
    column_editable_list = ('name', 'retail_shop_id')
    column_filters = ('products.name', 'retail_shop')

    form_ajax_refs = {
        'products': QueryAjaxModelLoader('products', db.session, Product, fields=['name'], page_size=10),
        'retail_shop': QueryAjaxModelLoader('retail_shop', db.session, RetailShop, fields=['name'], page_size=10),
    }


class SaltAdmin(MyModel):
    column_sortable_list = ('name',)
    column_searchable_list = ('id', 'retail_shop_id', 'name')
    column_editable_list = ('name', 'retail_shop_id')
    column_filters = ('products.name', 'retail_shop')

    form_ajax_refs = {
        'products': QueryAjaxModelLoader('products', db.session, Product, fields=['name'], page_size=10),
        'retail_shop': QueryAjaxModelLoader('retail_shop', db.session, RetailShop, fields=['name'], page_size=10),
    }


class TagAdmin(MyModel):
    column_sortable_list = ('name',)
    column_searchable_list = ('id', 'retail_shop_id', 'name')
    column_editable_list = ('name', 'retail_shop_id')
    column_filters = ('products.name', 'retail_shop')

    form_ajax_refs = {
        'product': QueryAjaxModelLoader('product', db.session, Product, fields=['name'], page_size=10),
        'retail_shop': QueryAjaxModelLoader('retail_shop', db.session, RetailShop, fields=['name'], page_size=10),
    }


class BrandAdmin(MyModel):

    column_sortable_list = ('name',)
    column_searchable_list = ('id', 'retail_shop_id', 'name')
    column_editable_list = ('name', 'retail_shop_id')
    column_filters = ('products.name', 'retail_shop')

    form_ajax_refs = {
        'products': QueryAjaxModelLoader('products', db.session, Product, fields=['name'], page_size=10),
        'retail_shop': QueryAjaxModelLoader('retail_shop', db.session, RetailShop, fields=['name'], page_size=10),
        'distributors': QueryAjaxModelLoader('distributors', db.session, Distributor, fields=['name'], page_size=10)
    }


class BrandDistributorAdmin(MyModel):

    column_searchable_list = ('id', 'brand_id', 'distributor_id')


class StockAdmin(MyModel):

    column_filters = ('product.name', 'product.retail_shop')
    column_editable_list = ('selling_amount', 'purchase_amount', 'batch_number', 'expiry_date',
                            'is_sold', 'default_stock', 'units_purchased')

    form_ajax_refs = {
        'product': QueryAjaxModelLoader('product', db.session, Product, fields=['name'], page_size=10),
        'distributor_bill': QueryAjaxModelLoader('distributor_bill', db.session, DistributorBill,
                                                 fields=['distributor_name', 'retail_shop_name'], page_size=10)
    }


class ProductTaxAdmin(MyModel):
    column_filters = ('product.name', 'product.retail_shop', 'tax')
    column_searchable_list = ('product.name', 'product.retail_shop_id', 'product.retail_shop.name')
    form_ajax_refs = {
        'tax': QueryAjaxModelLoader('tax', db.session, Tax, fields=['name'], page_size=10),
        'products': QueryAjaxModelLoader('products', db.session, Product, fields=['name'], page_size=10),
    }


class ProductSaltAdmin(MyModel):
    column_filters = ('product.name', 'product.retail_shop', 'salt')
    column_searchable_list = ('product.name', 'product.retail_shop_id', 'product.retail_shop.name')

    form_ajax_refs = {
        'salt': QueryAjaxModelLoader('salt', db.session, Salt, fields=['name'], page_size=10),
        'product': QueryAjaxModelLoader('product', db.session, Product, fields=['name'], page_size=10),
    }


class ProductTagAdmin(MyModel):
    column_filters = ('product.name', 'product.retail_shop', 'tag')
    column_searchable_list = ('product.name', 'product.retail_shop_id', 'product.retail_shop.name')

    form_ajax_refs = {
        'tag': QueryAjaxModelLoader('tag', db.session, Tag, fields=['name'], page_size=10),
        'product': QueryAjaxModelLoader('product', db.session, Product, fields=['name'], page_size=10),
    }


admin.add_view(MyModel(User, session=db.session))
admin.add_view(MyModel(Customer, session=db.session))
admin.add_view(MyModel(CustomerTransaction, session=db.session))
admin.add_view(MyModel(Role, session=db.session))
admin.add_view(MyModel(UserRole, session=db.session))
admin.add_view(MyModel(Permission, session=db.session))

admin.add_view(RetailShopAdmin(RetailShop, session=db.session))
admin.add_view(MyModel(RetailBrand, session=db.session))
admin.add_view(MyModel(UserRetailShop, session=db.session))
admin.add_view(MyModel(RegistrationDetail, session=db.session))
admin.add_view(MyModel(PrinterConfig, session=db.session))
admin.add_view(MyModel(Address, session=db.session))
admin.add_view(MyModel(CustomerAddress, session=db.session))
admin.add_view(MyModel(Locality, session=db.session))
admin.add_view(MyModel(City, session=db.session))


admin.add_view(ProductAdmin(Product, session=db.session))
admin.add_view(TagAdmin(Tag, session=db.session))
admin.add_view(SaltAdmin(Salt, session=db.session))
admin.add_view(BrandAdmin(Brand, session=db.session))
admin.add_view(StockAdmin(Stock, session=db.session))
admin.add_view(DistributorAdmin(Distributor, session=db.session))
admin.add_view(TaxAdmin(Tax, session=db.session))

admin.add_view(ProductTaxAdmin(ProductTax, session=db.session))
admin.add_view(ProductSaltAdmin(ProductSalt, session=db.session))
admin.add_view(ProductTagAdmin(ProductTag, session=db.session))
admin.add_view(MyModel(AddOn, session=db.session))
admin.add_view(MyModel(Combo, session=db.session))
admin.add_view(MyModel(ProductType, session=db.session))
admin.add_view(DistributorBillAdmin(DistributorBill, session=db.session))
admin.add_view(BrandDistributorAdmin(BrandDistributor, session=db.session))


admin.add_view(MyModel(Order, session=db.session))
admin.add_view(MyModel(OrderStatus, session=db.session))
admin.add_view(MyModel(Item, session=db.session))
admin.add_view(MyModel(ItemTax, session=db.session))
admin.add_view(MyModel(ItemAddOn, session=db.session))
admin.add_view(MyModel(Status, session=db.session))
admin.add_view(MyModel(OrderDiscount, session=db.session))
admin.add_view(MyModel(Discount, session=db.session))
