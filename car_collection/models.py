from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime


from werkzeug.security import generate_password_hash, check_password_hash


import secrets

from flask_login import UserMixin, LoginManager

from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    car = db.relationship('Car', backref = 'owner', lazy = True)
    

    def __init__(self,email,first_name = '', last_name = '', id = '', password = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token()
    
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self):
        return secrets.token_hex()

    def __repr__(self):
        return f'User {self.email} has been added to the database'
    

class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    make = db.Column(db.String(150))
    model = db.Column(db.String(150))
    year = db.Column(db.Numeric(precision=10, scale=2))
    color = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision=10, scale=2))
    miles_per_gallon = db.Column(db.String(150))
    max_speed = db.Column(db.String(100))
    seats = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, make, model, year, color, description, price, miles_per_gallon, max_speed,
                 seats, user_token):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.description = description
        self.price = price
        self.miles_per_gallon = miles_per_gallon
        self.max_speed = max_speed
        self.seats = seats
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    

    def __repr__(self):
        return f"Car added."


class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'make', 'model', 'year', 'color', 'description',
                  'price', 'miles_per_gallon', 'max_speed', 'seats']
        
car_schema = CarSchema()
cars_schema = CarSchema(many = True)