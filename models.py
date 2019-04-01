import datetime

from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('message.db')

class User(UserMixin, Model):
    fname = CharField()
    lname = CharField()
    email = CharField(unique=True)
    password = CharField(max_length=100)
    # street_address = CharField()
    # city = CharField()
    # state = CharField()
    # postal_code = IntegerField()
    join_date = DateTimeField(default=datetime.datetime.now())

    @classmethod
    def create_user(cls, fname, lname, email, password):
        try:
            cls.create(
                fname = fname,
                lname = lname,
                email=email,
                # this function is from bcrypt
                password=generate_password_hash(password)
            )
        except IntegrityError:
            raise ValueError("user already exists")

    class Meta:
        database = DATABASE

class Category(Model):
    category_name = CharField(unique=True)
    class Meta:
        database = DATABASE

class Product(Model):
    name = CharField()
    description = CharField()
    image = CharField()
    meaning = CharField()
    price = IntegerField()
    category = ForeignKeyField(model=Category, backref='product')

    class Meta:
        database = DATABASE

class Order(Model):
    user = ForeignKeyField(model=User, backref='order')
    order_date = DateTimeField(default=datetime.datetime.now())
    total_cost = IntegerField(default=0)
    date_created = DateTimeField(default=datetime.datetime.now())
    purchased = BooleanField(default=False)
    class Meta:
        database = DATABASE

class OrderDetails(Model):
    order = ForeignKeyField(model=Order, backref='order_details')
    product = ForeignKeyField(model=Product, backref='order_details')
    quantity = IntegerField()

    class Meta:
        database = DATABASE

class Review(Model):
    user = ForeignKeyField(model=User, backref='review')
    product = ForeignKeyField(model=Product, backref='review')
    title = CharField()
    rating = IntegerField()
    content = CharField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Product, Category, Order, OrderDetails, Review], safe=True)
    DATABASE.close()
