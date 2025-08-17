from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ...extensions import db
from ...models import User
from ...forms import LoginForm, RegisterForm
auth_bp = Blueprint('auth', __name__, template_folder='../../templates/auth')

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated: return redirect(url_for("shop.home"))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data.lower()).first()
        if u and u.check_password(form.password.data):
            login_user(u, remember=form.remember.data); return redirect(url_for("shop.home"))
        flash("Invalid email or password", "danger")
    return render_template("auth/login.html", form=form)

@auth_bp.route("/register", methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("shop.home"))

    form = RegisterForm()
    if form.validate_on_submit():
        # Check if email already exists
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("Email already registered", "warning")
        else:
            # Create new user with name
            u = User(
                name=form.name.data,  # <-- add name here
                email=form.email.data.lower()
            )
            u.set_password(form.password.data)
            db.session.add(u)
            db.session.commit()
            flash("Account created. Please sign in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout(): logout_user(); return redirect(url_for("shop.home"))
