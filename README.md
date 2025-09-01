# 🛒 SwiftCart – E-Commerce Web App  

SwiftCart is a modern, lightweight, and responsive **Flask-based e-commerce platform** designed for fast and simple online shopping experiences. It features a clean UI, product management, and a smooth checkout flow.  

🌐 **Live Demo:** [swiftcart.xo.je](https://swiftcart.xo.je)  

---

## 🚀 Features  

- ✅ User-friendly storefront with product browsing  
- ✅ Dynamic product categories & search functionality  
- ✅ Shopping cart & order management  
- ✅ Admin dashboard for managing products and store settings  
- ✅ Built with **Flask + Jinja2** for backend & templating  
- ✅ Styled using **TailwindCSS** for responsive design  
- ✅ SQLite database (easily switchable to MySQL/PostgreSQL)  
- ✅ Deployed on **AWS EC2** with domain integration  

---

## 🏗️ Tech Stack  

**Frontend:**  
- HTML5, CSS3, JavaScript  
- TailwindCSS  

**Backend:**  
- Python (Flask Framework)  
- Jinja2 templating  

**Database:**  
- SQLite (development)  
- MySQL/PostgreSQL (production ready)  

**Deployment:**  
- AWS EC2 (Ubuntu)  
- Nginx + Gunicorn  
- GitHub for version control  

---

## ⚡ Installation & Setup  

Clone the repository:  
```bash
git clone https://github.com/your-username/swiftcart.git
cd swiftcart
```

Create & activate virtual environment:  
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

Install dependencies:  
```bash
pip install -r requirements.txt
```

Initialize database:  
```bash
flask db upgrade
```

Run the app locally:  
```bash
flask run
```

Visit 👉 `http://127.0.0.1:5000/`  

---

## 📸 Screenshots  

### 🏬 Homepage  
![Homepage](https://raw.githubusercontent.com/iamaindrik/swiftcart/main/screenshots/home.png)  

### 🛍️ Product Page  
![Product Page](https://raw.githubusercontent.com/iamaindrik/swiftcart/main/screenshots/product.png)  

### 🛒 Cart  
![Cart](https://raw.githubusercontent.com/iamaindrik/swiftcart/main/screenshots/cart.png)  

---

## 📦 Project Structure  

```
swiftcart/
│── app/
│   ├── models.py        # Database models
│   ├── routes.py        # App routes
│   ├── templates/       # Jinja2 templates
│   ├── static/          # CSS, JS, Images
│── migrations/          # Database migrations
│── requirements.txt     # Dependencies
│── config.py            # App configuration
│── run.py               # Entry point
```

---

## 🤝 Contributing  

Pull requests are welcome!  
If you’d like to improve SwiftCart, feel free to fork this repo and submit a PR.  

---

## 📜 License  

This project is licensed under the **MIT License** – you’re free to use and modify it.  

---

## ✨ Author  

👤 **Aindrik Sarkar**  
- Portfolio: [swiftcart.xo.je](iamaindrik.github.io)  
- GitHub: [@iamaindrik](https://github.com/iamaindrik)  
