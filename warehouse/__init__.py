from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy
# from warehouse import db
from flask_login import LoginManager,UserMixin
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
app.config['SECRET_KEY'] = 'thisistheprojectforarele'
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_message_category = 'info'
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(length=50), nullable=False)
    last_name = db.Column(db.String(length=50), nullable=False)
    password_hash = db.Column(db.String(length=50), nullable=False)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    items = db.relationship('Item', backref='owned_user',lazy=True)

    @property
    def password(self):
        return self.password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_return(self, item_obj):
        return item_obj in self.items

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Product = db.Column(db.String(length=50), nullable=False, unique=True)
    Quantity = db.Column(db.Integer(), nullable=False, default= None)
    Warehouse = db.Column(db.String(length=50), nullable=False, unique=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))


# class Item(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     Product = db.Column(db.String(length=30), nullable=False, unique=True)
#     Quantity = db.Column(db.Integer(), nullable=False, default= None)
#     Warehouse = db.Column(db.String(length=40), nullable=False, unique=True)

    # def __repr__(self):
    #     return f"Item('{self.Product}', '{self.Quantity}', '{self.Warehouse}')"


def transfer_to(self, user):
    self.owner = user.id
    # user.budget -= self.price
    db.session.commit()


def transfer(self, user):
    self.owner = NULL
    db.session.commit()

with app.app_context():
    db.create_all()



