from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from salesapp.app import db, app
from flask_login import UserMixin
import enum


class UserRole(enum.Enum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(1000),
                    default="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg")
    role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name

class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    image = Column(String(100))
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib
        u = User(name="Admin", username="admin",
                 password=hashlib.md5("123456".encode("utf-8")).hexdigest(),
                 role=UserRole.ADMIN)
        db.session.add(u)
        # c1 = Category(name="Mobile")
        # c2 = Category(name="Tablet")
        # p1 = Product(name="iPhone 7 Plus", price=17000000,
        #              image="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647056401/ipmsmnxjydrhpo21xrd8.jpg",
        #              category_id=1)
        # p2 = Product(name="iPad Pro 2020", price=37000000,
        #              image="https://res.cloudinary.com/dxxwcby8l/image/upload/v1646729533/zuur9gzztcekmyfenkfr.jpg",
        #              category_id=2)
        # p3 = Product(name="Galaxy Note 10 Plus", price=24000000,
        #              image="https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg",
        #              category_id=1)
        # # db.session.add(c1)
        # # db.session.add(c2)
        # db.session.add_all([p1, p2, p3])
        db.session.commit()
