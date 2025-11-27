from market import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email_address = db.Column(db.String(50), nullable=False, unique=True)   # ✅ FIXED NAME
    password_hash = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer, nullable=False ,default=5000000)
    is_admin = db.Column(db.Boolean, default=False)

    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plain_pass):
        self.password_hash = bcrypt.generate_password_hash(plain_pass).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item):
        return self.budget >= item.price

    def can_sell(self, item):
        return item in self.items

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    barcode = db.Column(db.String(12), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False)
    image = db.Column(db.String(200), nullable=True)   # ✅ NEW
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))


    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()

image_url = db.Column(db.String(200), nullable=True)

image = db.Column(db.String(200), nullable=True)

