from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose
from salesapp.app import app, db
from salesapp.app.model import Category, Product
from flask_login import current_user, logout_user
from flask import redirect

admin = Admin(app=app, name="Quản lý bán hàng", template_mode='bootstrap4')


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyProductView(AuthenticatedAdmin):
    column_list = ['id', 'name', 'price']
    can_export = True
    column_searchable_list = ["name"]
    column_filters = ['name', 'price']
    column_editable_list = ["name", "price"]
    details_modal = True
    edit_modal = True


class MyCategoryView(AuthenticatedAdmin):
    column_list = ['name', 'products']


class MyStatsView(AuthenticatedUser):
    @expose("/")
    def index(self):
        return self.render("admin/stats.html")


class MyLogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")


admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(MyStatsView(name="Thống kê báo cáo"))
admin.add_view(MyLogoutView(name="Đăng xuất"))
