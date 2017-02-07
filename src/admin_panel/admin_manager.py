from flask_admin_impexp.admin_impexp import AdminImportExport

from src import admin, db
from src.user.models import User, Role, PermissionSet, UserRole, RetailBrand, RetailShop, UserRetailShop, \
    Address, Locality, City, Customer
from src.orders.models import OrderDiscount, OrderItemTax, OrderItem, Order, Discount
from src.products.models import ProductTax, Tax, Product, ProductType, Stock, Distributor,\
    DistributorBill, Tag, Brand


class MyModel(AdminImportExport):
    page_size = 100
    column_display_pk = True
    pass


class RetailShopAdmin(MyModel):

    form_excluded_columns = ('products', 'orders', 'brands', 'distributors')

admin.add_view(MyModel(User, session=db.session))
admin.add_view(MyModel(Customer, session=db.session))
admin.add_view(MyModel(Role, session=db.session))
admin.add_view(MyModel(UserRole, session=db.session))
admin.add_view(MyModel(PermissionSet, session=db.session))
admin.add_view(RetailShopAdmin(RetailShop, session=db.session))
admin.add_view(MyModel(RetailBrand, session=db.session))
admin.add_view(MyModel(UserRetailShop, session=db.session))
admin.add_view(MyModel(Address, session=db.session))
admin.add_view(MyModel(Locality, session=db.session))
admin.add_view(MyModel(City, session=db.session))

admin.add_view(MyModel(ProductTax, session=db.session))
admin.add_view(MyModel(Tag, session=db.session))
admin.add_view(MyModel(Brand, session=db.session))
admin.add_view(MyModel(Tax, session=db.session))
admin.add_view(MyModel(Product, session=db.session))
admin.add_view(MyModel(ProductType, session=db.session))
admin.add_view(MyModel(Distributor, session=db.session))
admin.add_view(MyModel(DistributorBill, session=db.session))
admin.add_view(MyModel(Stock, session=db.session))


admin.add_view(MyModel(Order, session=db.session))
admin.add_view(MyModel(OrderItem, session=db.session))
admin.add_view(MyModel(OrderItemTax, session=db.session))
admin.add_view(MyModel(OrderDiscount, session=db.session))
admin.add_view(MyModel(Discount, session=db.session))
