from flask_admin_impexp.admin_impexp import AdminImportExport
from flask_security import current_user
from src import admin, db
from src.user.models import User, Role, Permission, UserRole, RetailBrand, RetailShop, UserRetailShop, \
    Address, Locality, City, Customer, RegistrationDetail, CustomerAddress, CustomerTransaction
from src.orders.models import OrderDiscount, Status, Item, ItemAddOn, Order, Discount, ItemTax
from src.products.models import ProductTax, Tax, Product, ProductType, Stock, Distributor,\
    DistributorBill, Tag, Brand, Salt, AddOn, Combo, ProductSalt


class MyModel(AdminImportExport):
    page_size = 100

    def is_accessible(self):
        return current_user.has_role('admin')


class RetailShopAdmin(MyModel):

    form_excluded_columns = ('products', 'orders', 'brands', 'distributors')


class DistributorBillAdmin(MyModel):

    form_excluded_columns = ('purchased_items',)

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
admin.add_view(MyModel(Address, session=db.session))
admin.add_view(MyModel(CustomerAddress, session=db.session))
admin.add_view(MyModel(Locality, session=db.session))
admin.add_view(MyModel(City, session=db.session))

admin.add_view(MyModel(ProductTax, session=db.session))
admin.add_view(MyModel(Tag, session=db.session))
admin.add_view(MyModel(AddOn, session=db.session))
admin.add_view(MyModel(Combo, session=db.session))
admin.add_view(MyModel(Salt, session=db.session))
admin.add_view(MyModel(ProductSalt, session=db.session))
admin.add_view(MyModel(Brand, session=db.session))
admin.add_view(MyModel(Tax, session=db.session))
admin.add_view(MyModel(Product, session=db.session))
admin.add_view(MyModel(ProductType, session=db.session))
admin.add_view(MyModel(Distributor, session=db.session))
admin.add_view(DistributorBillAdmin(DistributorBill, session=db.session))
admin.add_view(MyModel(Stock, session=db.session))


admin.add_view(MyModel(Order, session=db.session))
admin.add_view(MyModel(Item, session=db.session))
admin.add_view(MyModel(ItemTax, session=db.session))
admin.add_view(MyModel(ItemAddOn, session=db.session))
admin.add_view(MyModel(Status, session=db.session))
admin.add_view(MyModel(OrderDiscount, session=db.session))
admin.add_view(MyModel(Discount, session=db.session))
