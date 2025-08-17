import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///mercado.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")

    # ✅ Central list of categories (Flipkart-style bar)
    CATEGORIES = [
        "Mobiles & Tablets",
        "TVs & Appliances",
        "Electronics",
        "Fashion",
        "Home & Kitchen",
        "Beauty & Toys",
        "Furniture",
        "Flight Bookings",
    ]


class Dev(Config):
    DEBUG = True


class Prod(Config):
    DEBUG = False
