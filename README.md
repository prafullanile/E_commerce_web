📦 Flask Market App

A complete marketplace web application built with Flask, allowing users to register, login, buy items, sell items, and manage products from an admin dashboard.
The project includes authentication, product management, image uploads, and a fully functional frontend UI.

🚀 Features
👤 User Features

Register & Login with secure password hashing (Flask-Bcrypt)

Browse products

Search & Filter items

Purchase items (money deducted from wallet)

Sell owned items (money added to wallet)

View personal owned items

Mobile-friendly UI

🔐 Admin Features

Admin-only dashboard

Add new products with images

Edit existing products

Delete products

Manage all users & items

🛒 Product System

Products stored in a database

Each item has:

Image

Name

Price

Description

Barcode

Ownership info

🔒 Authentication

Login system using Flask-Login

Password hashing using Flask-Bcrypt

CSRF protection with Flask-WTF

🛠️ Tech Stack
Backend

Flask

Flask-SQLAlchemy

Flask-WTF

Flask-Login

Flask-Bcrypt

Database

SQLite3

Frontend

HTML, CSS, Bootstrap

Jinja2 Templates

📁 Project Folder Structure
market/
│── __init__.py          # App configuration, DB setup, login manager
│── models.py            # Database models (User, Item)
│── forms.py             # Forms for login, register, purchase, sell
│── routes.py            # All application routes & logic
│── static/
│     ├── product_images # Uploaded product images
│     └── css, js, icons
│── templates/
      ├── base.html
      ├── home.html
      ├── market.html
      ├── login.html
      ├── register.html
      ├── admin/
      │     ├── admin_dashboard.html
      │     ├── add_item.html
      │     └── edit_item.html
      └── includes/
            ├── items_modals.html

⚙️ Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/YOUR_USERNAME/market-app.git
cd market-app

2️⃣ Create a virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Initialize the database

Open Python shell:

python
>>> from market import db
>>> db.create_all()
>>> exit()

5️⃣ Run the server
python run.py


Visit the app in browser:

http://127.0.0.1:5000/

🧪 Admin Login Setup

Inside Python shell:

from market.models import User
from market import db

admin = User(username="admin", email_address="admin@gmail.com", password="admin123")
admin.is_admin = True

db.session.add(admin)
db.session.commit()

🖼️ Screenshots (Add when you upload)

You can add images like:

![Home Page](screenshots/home.png)
![Market Page](screenshots/market.png)
![Admin Dashboard](screenshots/admin.png)

💡 How Buying/Selling Works
Buy:

Checks user has enough money

Sets item.owner = user.id

Deducts price from user budget

Sell:

Sets item.owner = None

Adds price to user budget
All handled in Item.buy() and Item.sell() methods.

🏆 Author
Prafull Nile
