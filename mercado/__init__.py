from flask import Flask
from .config import Dev
from .extensions import db, login_manager, migrate
from .models import User
from .blueprints.auth.routes import auth_bp
from .blueprints.shop.routes import shop_bp
from .blueprints.admin.routes import admin_bp


def create_app(config_object=Dev):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    # --- Init extensions ---
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # --- Flask-Login user loader ---
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(int(uid))

    login_manager.login_view = "auth.login"

    # --- Register blueprints ---
    app.register_blueprint(auth_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # --- Inject categories into all templates ---
    @app.context_processor
    def inject_categories():
        names = app.config.get("CATEGORIES", [])
        cats = [{"id": i + 1, "name": name} for i, name in enumerate(names)]
        return {"categories": cats}

    return app
