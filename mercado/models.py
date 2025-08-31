from datetime import datetime
from .extensions import db
from flask_login import UserMixin
import math
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # one-to-many relation: a category can have many products
    products = db.relationship("Product", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, default="")
    price = db.Column(db.Float, nullable=False, default=0.0)
    discount_percent = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(600), default="")
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 🔗 category_id foreign key
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)

    # @property
    # def sale_price(self):
    #     if self.discount_percent and self.discount_percent > 0:
    #         return round(self.price * (1 - self.discount_percent / 100), 2)
    #     return round(self.price or 0, 2)
    
    @property
    def sale_price(self):
        if self.discount_percent and self.discount_percent > 0:
            raw_price = self.price * (1 - self.discount_percent / 100)
            # round down to nearest whole number
            base = math.floor(raw_price)
            # adjust to nearest xx99 (psychological pricing)
            if base > 99:
                return (base // 100) * 100 + 99
            else:
                return base
        return round(self.price or 0, 2)


class AdminSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(120), default="SwiftCart")
    brand_subtext = db.Column(db.String(255), default="Modern deals, fast checkout.")
    razorpay_key_id = db.Column(db.String(200), default="")
    razorpay_key_secret = db.Column(db.String(200), default="")


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    customer_name = db.Column(db.String(120), nullable=False)
    customer_email = db.Column(db.String(180), nullable=False)
    customer_phone = db.Column(db.String(30), nullable=True)
    address_line1 = db.Column(db.String(180), nullable=False)
    address_line2 = db.Column(db.String(180), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    razorpay_order_id = db.Column(db.String(200))
    razorpay_payment_id = db.Column(db.String(200))
    total_amount = db.Column(db.Float, default=0.0)

    items = db.relationship(
        "OrderItem", backref="order", lazy=True, cascade="all, delete-orphan"
    )


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product_title = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price_each = db.Column(db.Float, default=0.0)

