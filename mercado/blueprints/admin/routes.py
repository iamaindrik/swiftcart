from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ...extensions import db
from ...models import Product, AdminSettings, Order
from ...forms import ProductForm, SettingsForm
from ...config import Config
from mercado.models import Category   # ⬅️ import category config

admin_bp = Blueprint('admin', __name__, template_folder='../../templates/admin')


def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*a, **k):
        if not current_user.is_authenticated or not getattr(current_user, "is_admin", False):
            flash("Admin access required.", "warning")
            return redirect(url_for("auth.login"))
        return fn(*a, **k)
    return wrapper


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    stats = {
        "products": Product.query.count(),
        "orders": Order.query.count(),
        "pending": Order.query.filter_by(status="Pending").count(),
        "paid": Order.query.filter_by(status="Paid").count(),
        "shipped": Order.query.filter_by(status="Shipped").count(),
    }
    latest_orders = Order.query.order_by(Order.created_at.desc()).limit(8).all()
    latest_products = Product.query.order_by(Product.id.desc()).limit(8).all()
    return render_template("admin/dashboard.html",
                           stats=stats,
                           latest_orders=latest_orders,
                           latest_products=latest_products)


@admin_bp.route("/products")
@login_required
@admin_required
def products():
    items = Product.query.order_by(Product.id.desc()).all()
    return render_template("admin/products.html", items=items)


@admin_bp.route("/products/new", methods=["GET", "POST"])
@login_required
@admin_required
def product_new():
    form = ProductForm()

    # 🔥 populate category dropdown from Config
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        p = Product(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            discount_percent=form.discount_percent.data or 0,
            image_url=form.image_url.data,
            is_featured=form.is_featured.data,
            category_id=form.category_id.data,   # ⬅️ save category
        )
        db.session.add(p)
        db.session.commit()
        flash("Product created.", "success")
        return redirect(url_for("admin.products"))
    return render_template("admin/product_form.html", form=form, is_new=True)


@admin_bp.route("/products/<int:pid>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def product_edit(pid):
    p = Product.query.get_or_404(pid)
    form = ProductForm(obj=p)

    # 🔥 populate category dropdown again for editing
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        form.populate_obj(p)
        if form.discount_percent.data is None:
            p.discount_percent = 0
        db.session.commit()
        flash("Product updated.", "success")
        return redirect(url_for("admin.products"))
    return render_template("admin/product_form.html", form=form, is_new=False)


@admin_bp.route("/products/<int:pid>/delete", methods=["POST"])
@login_required
@admin_required
def product_delete(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    flash("Product deleted.", "success")
    return redirect(url_for("admin.products"))


@admin_bp.route("/settings", methods=["GET", "POST"])
@login_required
@admin_required
def settings():
    s = AdminSettings.query.first()
    if not s:
        s = AdminSettings()
        db.session.add(s)
        db.session.commit()
    form = SettingsForm(obj=s)
    if form.validate_on_submit():
        form.populate_obj(s)
        db.session.commit()
        flash("Settings saved.", "success")
        return redirect(url_for("admin.settings"))
    return render_template("admin/settings.html", form=form)


@admin_bp.route("/orders")
@login_required
@admin_required
def orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin/orders.html", orders=orders)


@admin_bp.route("/orders/<int:oid>")
@login_required
@admin_required
def order_detail(oid):
    order = Order.query.get_or_404(oid)
    return render_template("admin/order_detail.html", order=order)


@admin_bp.route("/orders/<int:oid>/status", methods=["POST"])
@login_required
@admin_required
def order_status(oid):
    order = Order.query.get_or_404(oid)
    new_status = request.form.get("status")
    if new_status in {"Pending", "Paid", "Shipped", "Delivered", "Cancelled"}:
        order.status = new_status
        db.session.commit()
        flash("Status updated.", "success")
    return redirect(url_for("admin.order_detail", oid=oid))


@admin_bp.route("/orders/<int:oid>/print")
@login_required
@admin_required
def order_print(oid):
    order = Order.query.get_or_404(oid)
    return render_template("admin/order_print.html", order=order)
