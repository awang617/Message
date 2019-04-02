
# import flask framework. g stands for global allows us to use other variable in the project
from flask import Flask, g, request
from flask import render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_bcrypt import check_password_hash
import datetime

import models
import forms

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = "peonies"

# setup login_manager with LoginManager class
login_manager = LoginManager()
# setup login_manager to work with our app
login_manager.init_app(app)
# if a user is not logged in, redirect them to login view
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try: 
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """Close the database after each connection requesst and send through the response"""
    g.db.close()
    return response

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash('This email does not exist.')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)    # creates a session and logs in the user
                flash('You have been logged in!', 'success')
                order = models.Order.select().where(models.Order.user == user.id, models.Order.purchased==False)
                if order.exists():
                    return redirect(url_for('shop'))
                else:
                    newOrder = models.Order.create_order(user=user)
                    return redirect(url_for('shop'))
            else:
                flash('Email or password incorrect.', 'danger')
    return render_template("login.html", form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.RegisterForm()
    # when the form is validated and submitted, create a new user
    if form.validate_on_submit():
        models.User.create_user(
            fname=form.fname.data,
            lname=form.lname.data,
            email=form.email.data,
            password=form.password.data
        )
        user = models.User.get(models.User.email== form.email.data)
        models.Order.create_order(user=user)
        login_user(user)
        # redirect user to index
        return redirect(url_for('shop'))
    return render_template("signup.html", form=form)

@app.route('/logout')
# from login_manager login view, will redirect you to the login page
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    user = current_user
    return render_template("profile.html", user=user)

@app.route('/shop', methods=["GET"])
@login_required
def shop():
    product = models.Product.select()
    return render_template("shop.html", product=product)

@app.route('/shop/<data_name>', methods=["GET"])
@login_required
def product_details(data_name):
    product = models.Product.get(models.Product.data_name == data_name)
    print(product)
    return render_template("productDetails.html", product=product)

@app.route('/cart', methods=["GET"])
@login_required
def cart():
    return render_template("cart.html")

if __name__ == '__main__':
    models.initialize()
    # try:
    #     models.Category.create(category_name="bouquet")
    #     models.Category.create(category_name="plant")
    #     bouquet = models.Category.get(models.Category.category_name == "bouquet")
    #     plant = models.Category.get(models.Category.category_name == "plant")
    #     models.Product.create(
    #         name="Roses are Red",
    #         description="Everyone knows red roses means love. This classic bouquet is perfect for romantic occasions.",
    #         image="https://cdn.azflorist.com/wp-content/uploads/20190128091943/E2-4305D.jpg",
    #         plant="red rose",
    #         meaning="love",
    #         price=40,
    #         data_name="red-roses",
    #         category=bouquet
    #     )
    #     models.Product.create(
    #         name="Prettily Presuming",
    #         description="Be careful when giving or recieving this beautiful bloom, as snapdragons mean presumption. Perhaps there is someone sets themselves too highly, or took you for granted. A snapdragon may snap them into place.",
    #         image="https://cdn1.harryanddavid.com/wcsstore/HarryAndDavid/images/catalog/17_31841_30E_01ex.jpg",
    #         plant="snapdragon",
    #         meaning="Presumption",
    #         price=35,
    #         data_name="prettily-presuming",
    #         category=bouquet
    #     )
    #     models.Product.create(
    #         name="Return of Happiness",
    #         description="These delicate flowers are perfect if you wish for a return of joy. Send it after an argument has pass or as a homecoming gift.",
    #         image="https://i.pinimg.com/originals/64/7e/b5/647eb574340a0351ba55e3d1d91fae77.jpg",
    #         plant="lily of the valley",
    #         meaning="Return of happiness",
    #         price=49,
    #         data_name="return-of-happiness",
    #         category=bouquet
    #     )
    #     models.Product.create(
    #         name="Ardent Love",
    #         description="Don't let its prickly exterior fool you. Cactus means ardent love, and is a great alternative if your partner thinks roses are cliche. Best of all, they are easy to care for and live long lives.",
    #         image="https://cdn.shopify.com/s/files/1/0130/1052/products/DSC_0340_1024x1024@2x.jpg?v=1517494867",
    #         plant="cactus",
    #         meaning="ardent love",
    #         price="19",
    #         data_name="ardent-love",
    #         category=plant
    #     )
    #     models.Product.create(
    #         name="Prosper",
    #         description="A gift imbued with the best wishes of prosperity and good health.",
    #         image="https://cdn.shopify.com/s/files/1/0207/8508/products/2018-Sage-Bush-001_1_1024x1024.jpg?v=1537882781",
    #         plant="sage",
    #         meaning="good health and long life",
    #         price=15,
    #         data_name="prosper",
    #         category=plant
    #     )
    #     models.Product.create(
    #         name="Lavender",
    #         description="Although its scent is soothing its meaning is not. Lavender means mistrust, so be wary who you send one to.",
    #         image="https://bouqs-production-weblinc.netdna-ssl.com/product_images/lavender/Original/5c3d2db061707040b4002757/detail.jpg?c=1547513264",
    #         plant="lavender",
    #         meaning="mistrust",
    #         price=22,
    #         data_name="potted-lavender",
    #         category=plant
    #     )
    # except ValueError:
    #     pass
    app.run(debug=DEBUG, port=PORT)
