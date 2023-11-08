from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from salesapp.app import app, db
from salesapp.app.model import Category, Product

admin = Admin(app=app, name="Quản lý bán hàng", template_mode='bootstrap4')

admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Product, db.session))