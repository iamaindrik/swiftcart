from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app, jsonify
from flask_login import login_required, current_user
from ...extensions import db
from ...models import Product, AdminSettings, Order, OrderItem, Category
from ...forms import AddressForm
import razorpay
from ...config import Config

shop_bp = Blueprint('shop', __name__, template_folder='../../templates/shop')

@shop_bp.app_template_filter('inr')
def inr(amount):
    return f"₹{amount:,.2f}"

def _cart():
    return session.get("cart", {})

# ---------------- Home ----------------
@shop_bp.route("/")
def home():
    settings = AdminSettings.query.first()
    if not settings:
        settings = AdminSettings()
        db.session.add(settings)
        db.session.commit()

    featured = Product.query.filter_by(is_featured=True).order_by(Product.id.desc()).limit(8).all()
    sale = Product.query.filter(Product.discount_percent > 0).order_by(Product.id.desc()).limit(8).all()
    latest = Product.query.order_by(Product.id.desc()).limit(8).all()

    categories = Category.query.order_by(Category.name.asc()).all()
    return render_template(
        "shop/home.html",
        settings=settings,
        featured=featured,
        sale=sale,
        latest=latest,
        categories=categories
    )

# ---------------- Category Page ----------------
@shop_bp.route("/category/<int:cid>")
def category(cid):
    category = Category.query.get_or_404(cid)
    products = Product.query.filter_by(category_id=cid).all()
    return render_template("shop/category.html", category=category, products=products)


# ---------------- Product Detail ----------------
@shop_bp.route("/p/<int:pid>")
def product_detail(pid):
    p = Product.query.get_or_404(pid)
    return render_template("shop/product_detail.html", p=p)

# ---------------- Cart ----------------
@shop_bp.route("/cart")
def view_cart():
    ids = [int(k) for k in _cart().keys()]
    products = Product.query.filter(Product.id.in_(ids)).all() if ids else []
    items, total, qmap = [], 0.0, {int(k): int(v) for k, v in _cart().items()}
    for p in products:
        qty = qmap.get(p.id, 1)
        price = p.sale_price * qty
        items.append((p, qty, price))
        total += price
    return render_template("shop/cart.html", items=items, total=total)

@shop_bp.route("/add_to_cart/<int:pid>")
def add_to_cart(pid):
    cart = _cart()
    cart[str(pid)] = cart.get(str(pid), 0) + 1
    session["cart"] = cart
    flash("Added to cart.", "success")
    return redirect(request.referrer or url_for("shop.view_cart"))

@shop_bp.route("/update_cart", methods=["POST"])
def update_cart():
    cart = {}
    for key, val in request.form.items():
        if key.startswith("qty_"):
            pid = key.split("_", 1)[1]
            try:
                qty = max(0, int(val))
            except:
                qty = 1
            if qty > 0:
                cart[pid] = qty
    session["cart"] = cart
    flash("Cart updated.", "success")
    return redirect(url_for("shop.view_cart"))

@shop_bp.route("/remove_from_cart/<int:pid>")
def remove_from_cart(pid):
    cart = _cart()
    cart.pop(str(pid), None)
    session["cart"] = cart
    flash("Removed.", "success")
    return redirect(url_for("shop.view_cart"))

# ---------------- Wishlist ----------------
@shop_bp.route("/wishlist")
def wishlist():
    ids = [int(x) for x in session.get("wishlist", [])]
    products = Product.query.filter(Product.id.in_(ids)).all() if ids else []
    return render_template("shop/wishlist.html", products=products)

@shop_bp.route("/toggle_wishlist/<int:pid>")
def toggle_wishlist(pid):
    wl = set(session.get("wishlist", []))
    if pid in wl:
        wl.remove(pid)
        flash("Removed from wishlist.", "success")
    else:
        wl.add(pid)
        flash("Added to wishlist.", "success")
    session["wishlist"] = list(wl)
    return redirect(request.referrer or url_for("shop.wishlist"))

# ---------------- Checkout ----------------
@shop_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart = _cart()
    if not cart:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("shop.home"))

    ids = [int(k) for k in cart.keys()]
    products = Product.query.filter(Product.id.in_(ids)).all()
    qmap = {int(k): int(v) for k, v in cart.items()}
    total = sum(p.sale_price * qmap.get(p.id, 1) for p in products)

    form = AddressForm()
    if form.validate_on_submit():
        order = Order(
            user_id=current_user.id,
            customer_name=form.customer_name.data,
            customer_email=form.customer_email.data,
            customer_phone=form.customer_phone.data,
            address_line1=form.address_line1.data,
            address_line2=form.address_line2.data,
            city=form.city.data,
            state=form.state.data,
            pincode=form.pincode.data,
            total_amount=total,
            status="Pending"
        )
        db.session.add(order)
        db.session.flush()

        for p in products:
            qty = qmap.get(p.id, 1)
            db.session.add(OrderItem(
                order_id=order.id,
                product_id=p.id,
                product_title=p.title,
                quantity=qty,
                price_each=p.sale_price
            ))
        db.session.commit()

        settings = AdminSettings.query.first()
        key_id = (settings.razorpay_key_id if settings else None) or current_app.config.get("RAZORPAY_KEY_ID", "")
        key_secret = (settings.razorpay_key_secret if settings else None) or current_app.config.get("RAZORPAY_KEY_SECRET", "")

        if key_id and key_secret:
            client = razorpay.Client(auth=(key_id, key_secret))
            rzp_order = client.order.create({
                "amount": int(total * 100),
                "currency": "INR",
                "payment_capture": 1,
                "receipt": f"order_{order.id}"
            })
            order.razorpay_order_id = rzp_order.get("id")
            db.session.commit()
            return render_template("shop/pay_razorpay.html", order=order, key_id=key_id)
        else:
            order.status = "Paid"
            db.session.commit()
            session["cart"] = {}
            flash("Order placed (COD mode).", "success")
            return redirect(url_for("shop.order_success", oid=order.id))

    return render_template("shop/checkout.html", form=form, total=total)

# ---------------- Orders ----------------
@shop_bp.route("/order/success/<int:oid>")
@login_required
def order_success(oid):
    order = Order.query.get_or_404(oid)
    return render_template("shop/order_success.html", order=order)

@shop_bp.route("/payment/callback", methods=["POST"])
def payment_callback():
    oid = request.form.get("oid")
    payment_id = request.form.get("razorpay_payment_id")
    order = Order.query.get(int(oid)) if oid else None
    if order:
        order.razorpay_payment_id = payment_id
        order.status = "Paid"
        db.session.commit()
        session["cart"] = {}
        return redirect(url_for("shop.order_success", oid=order.id))
    return "OK", 200

# ---------------- API Search ----------------
@shop_bp.route('/api/search')
def api_search():
    query = request.args.get('q', '').strip()
    results = []
    if query:
        products = Product.query.filter(Product.title.ilike(f"%{query}%")).limit(8).all()
        results = [{
            "id": p.id,
            "title": p.title,
            "price": p.price,
            "image": p.image_url or f"https://picsum.photos/seed/{p.id}/100/100"
        } for p in products]
    return jsonify(results)

@shop_bp.route("/policies")
def policies():
    # Just render one page with all policies
    return render_template("shop/policies.html")
