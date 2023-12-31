import hashlib
from salesapp.app import app
from salesapp.app.model import Category, Product, User
import cloudinary.uploader


def get_categories():
    return Category.query.all()


def get_products(kw, cate_id, page=None):
    products = Product.query

    if kw:
        products = products.filter(Category.name.contains(kw))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    if page:
        page = int(page)
        page_size = app.config["PAGE_SIZE"]
        start = (page - 1) * page_size

        return products.slice(start, start + page_size)

    return products.all()


def count_products():
    return Product.query.count()


def get_user_by_user_id(user_id):
    return User.query.get(user_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def add_user(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())

    u = User(username=username, password=password, name=name)
    if avatar:
        avatar = cloudinary.uploader.upload(avatar)
        u.avatar(avatar)
    else:
        pass

