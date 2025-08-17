# SwiftCart (Flask) — Full Starter

Features:
- Auth (register/login/logout)
- Products (CRUD, featured, discount, images)
- Responsive cards with image auto-fit
- Cart + Wishlist (session-based)
- Checkout with address form
- Orders saved to DB with statuses (Pending, Paid, Shipped, Delivered, Cancelled)
- Razorpay checkout (if keys configured) else COD fallback
- Admin panel: dashboard, products, orders (status updates), printable invoice
- SQLite + Flask-Migrate

## Quickstart
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows
# or: source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# DB
flask db init
flask db migrate -m "init"
flask db upgrade

# Create admin:
python -c "from mercado import create_app; from mercado.extensions import db; from mercado.models import User; a=create_app(); with a.app_context(): u=User(email='admin@example.com', is_admin=True); u.set_password('admin123'); db.session.add(u); db.session.commit(); print('admin created')"

# Run
python app.py
```
Admin at `/admin`. Razorpay keys can be saved under **Admin → Settings**.
