import datetime

from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash
import os
import psycopg2

from playhouse.db_url import connect

# DATABASE = connect(os.environ.get('DATABASE_URL'))

DATABASE = PostgresqlDatabase('message')

class User(UserMixin, Model):
    fname = CharField()
    lname = CharField()
    email = CharField(unique=True)
    password = CharField(max_length=100)
    street_address = CharField(default="")
    city = CharField(default="")
    state = CharField(default="")
    postal_code = CharField(default="")
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
    name = CharField(unique=True)
    description = CharField()
    image = CharField()
    plant = CharField()
    meaning = CharField()
    price = IntegerField()
    data_name= CharField()
    average_rating = FloatField(default=0)
    category = ForeignKeyField(model=Category, backref='product')

    class Meta:
        database = DATABASE

class Order(Model):
    user = ForeignKeyField(model=User, backref='order')
    order_date = DateTimeField(default=datetime.datetime.now())
    total_cost = IntegerField(default=0)
    date_created = DateTimeField(default=datetime.datetime.now())
    recipient_fname = CharField(default="")
    recipient_lname = CharField(default="")
    recipient_street_address = CharField(default="")
    recipient_city = CharField(default="")
    recipient_state = CharField(default="")
    recipient_postal_code = CharField(default="")
    purchased = BooleanField(default=False)

    @classmethod
    def create_order(cls, user):
        try:
            cls.create(
                user = user
            )
        except:
            raise ValueError("order error")

    class Meta:
        database = DATABASE

class OrderDetails(Model):
    order = ForeignKeyField(model=Order, backref='order_details')
    product = ForeignKeyField(model=Product, backref='order_details')
    quantity = IntegerField(default=1)
    subtotal = IntegerField()

    @classmethod
    def create_order_details(cls, order, product, subtotal):
        try:
            cls.create(
                order=order,
                product=product,
                subtotal=subtotal
            )
        except:
            raise ValueError("add to cart error")

    class Meta:
        database = DATABASE

class Review(Model):
    user = ForeignKeyField(model=User, backref='review')
    product = ForeignKeyField(model=Product, backref='review')
    title = CharField()
    rating = IntegerField()
    content = CharField()
    date_posted = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Product, Category, Order, OrderDetails, Review], safe=True)
    DATABASE.close()
