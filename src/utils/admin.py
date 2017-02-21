from flask import url_for, redirect
from flask_admin import Admin, AdminIndexView
from flask_admin import expose
from flask_security import current_user


class MyAdminIndexView(AdminIndexView):

    def __init__(self, endpoint=None, url=None,):
        super(MyAdminIndexView, self).__init__(url=url, endpoint=endpoint)

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('security.login'))
        return super(MyAdminIndexView, self).index()

admin = Admin(name="Open POS", template_mode='bootstrap3', index_view=MyAdminIndexView(url='/admin'))
