
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

def time_of_day(hour):
    return (
        "morning" if 5 <= hour <= 11
        else
        "afternoon" if 12 <= hour <= 17
        else
        "evening" if 18 <= hour <= 22
        else
        "night"
    )

@app.route('/profile')
@login_required
def profile():
    user = current_user
    current_hour = datetime.datetime.now().hour
    greeting = time_of_day(current_hour)
    return render_template("dashboard.html", user=user, greeting=greeting)


@app.route('/profile/orders', methods=["GET"])
@login_required
def order_history():
    user = current_user
    current_hour = datetime.datetime.now().hour
    greeting = time_of_day(current_hour)
    orders = models.Order.select().where(models.Order.user_id == user.id, models.Order.purchased == True)
    return render_template("orderHistory.html", user=user, greeting=greeting, orders=orders)

@app.route('/profile/orders/view_details/<orderid>', methods=["GET"])
@login_required
def view_details(orderid):
    user = current_user
    current_hour = datetime.datetime.now().hour
    greeting = time_of_day(current_hour)
    order = models.Order.get(models.Order.id == orderid)
    print(order)
    details = models.OrderDetails.select().where(models.OrderDetails.order_id == orderid)
    return render_template("viewDetails.html", user=user, greeting=greeting, order=order, details=details)

@app.route('/profile/reviews', methods=["GET"])
@login_required
def reviews():
    user = current_user
    current_hour = datetime.datetime.now().hour
    greeting = time_of_day(current_hour)
    reviews = models.Review.select().where(models.Review.user_id == user.id)
    return render_template("reviews.html", user=user, greeting=greeting, reviews=reviews)

@app.route('/profile/reviews/review_details/<reviewid>', methods=["GET"])
@login_required
def review_details(reviewid):
    user = current_user
    current_hour = datetime.datetime.now().hour
    greeting = time_of_day(current_hour)
    review = models.Review.get(models.Review.id == reviewid)
    return render_template("reviewDetails.html", user=user, greeting=greeting, review=review)

@app.route('/delete_review/<reviewid>', methods=["GET", "DELETE", "PUT"])
def delete_review(reviewid):
    try:
        delete_review = models.Review.get(models.Review.id == reviewid)
    except:
        raise Exception("delete review error")
    if delete_review:
        print("this review's rating", delete_review.rating)
        product = models.Product.get(models.Product.id == delete_review.product_id)
        print("current product average", product.average_rating)
        delete_review.delete_instance()
        reviews = models.Review.select().where(models.Review.product_id == product.id)
        avg = "%.2f" % average(reviews)
        print("variable avg",avg)
        product.average_rating = avg
        product.save()
        print("new product average", product.average_rating)
        return redirect(url_for('reviews'))
    else:
        return("error")


@app.route('/shop', methods=["GET"])
@login_required
def shop():
    product = models.Product.select()
    return render_template("shop.html", product=product)

def average(reviews):
    ratings = []
    for review in reviews:
        print("from average(), ratings", review.rating)
        ratings.append(review.rating)
    if len(ratings)==0:
        return 0
    return sum(ratings)/len(ratings)

@app.route('/shop/<data_name>', methods=["GET", "POST"])
@login_required
def product_details(data_name):
    form = forms.ReviewForm()
    user = current_user
    product = models.Product.get(models.Product.data_name == data_name)
    reviews = models.Review.select().where(models.Review.product_id == product.id)
    if form.validate_on_submit():
        models.Review.create(
            user=user.id,
            product=product,
            title=form.title.data,
            rating=form.rating.data,
            content=form.content.data
        )
        avg = "%.2f" % average(reviews)
        product.average_rating = avg
        product.save()
        return redirect(url_for("product_details", data_name=data_name))
    # print(product)
    return render_template("productDetails.html", product=product, form=form, reviews=reviews)

def increment_total(price):
    user = current_user
    order = models.Order.select().where(models.Order.user == user.id, models.Order.purchased==False).get()
    order.total_cost += price
    order.save()

def decrement_total(price):
    user = current_user
    order = models.Order.select().where(models.Order.user == user.id, models.Order.purchased==False).get()
    order.total_cost -= price
    order.save()

@app.route('/add_to_cart/<productid>', methods=["GET", "POST", "PUT"])
@login_required
def add_to_cart(productid):
    user = current_user
    order = models.Order.select(models.Order.id).where(models.Order.user == user.id, models.Order.purchased==False)
    order_details = models.OrderDetails.select(models.Product, models.OrderDetails).join(models.Product).where(models.OrderDetails.order_id == order, models.OrderDetails.product_id == productid)
    if order_details.exists():
        existing_order_details = order_details.get()
        existing_order_details.quantity += 1
        existing_order_details.save()
        existing_order_details.subtotal += existing_order_details.product.price
        existing_order_details.save()
        increment_total(existing_order_details.product.price)
        return redirect(url_for("cart"))
    else:
        user = current_user
        product = models.Product.select().where(models.Product.id == productid).get()
        order = models.Order.select().where(models.Order.user == user.id, models.Order.purchased==False).get()
        try:
            models.OrderDetails.create_order_details(order.id, product.id, product.price)
            increment_total(product.price)
            return redirect(url_for("cart"))
        except:
            raise Exception("failed to add to cart")

@app.route('/subtract_from_cart/<order_details_id>', methods=["GET", "PUT"])
@login_required
def subtract_from_cart(order_details_id):
    order_details = models.OrderDetails.select().where(models.OrderDetails.id == order_details_id)
    if order_details.exists():
        existing_order_details = order_details.get()
        if existing_order_details.quantity > 1:
            existing_order_details.quantity -= 1
            existing_order_details.save()
            existing_order_details.subtotal -= existing_order_details.product.price
            existing_order_details.save()
            decrement_total(existing_order_details.product.price)
            return redirect(url_for("cart"))
        else:
            decrement_total(existing_order_details.product.price)
            existing_order_details.delete_instance()
            return redirect(url_for("cart"))
    else:
        flash("there was an error with this request")

@app.route('/remove_from_cart/<order_details_id>', methods=["GET", "DELETE"])
@login_required
def remove_from_cart(order_details_id):
    try:
        remove_order = models.OrderDetails.get(models.OrderDetails.id == order_details_id)
    except:
        raise Exception("remove from cart error")
    if remove_order:
        remove_order.order.total_cost -= remove_order.subtotal
        remove_order.order.save()
        remove_order.delete_instance()
        
        return redirect(url_for("cart"))
    else:
        return ("error")

@app.route('/cart', methods=["GET"])
@login_required
def cart():
    user = current_user
    order = models.Order.select().where(models.Order.user == user.id, models.Order.purchased==False).get()
    cart = models.OrderDetails.select().where(models.OrderDetails.order_id == order.id)
    
    return render_template("cart.html", cart=cart, order=order)

@app.route('/checkout', methods=["GET", "PUT"])
def checkout():
    user = current_user
    order = models.Order.get(models.Order.user_id == user.id, models.Order.purchased == False)
    print(order.purchased)
    order.purchased = True
    order.save()
    order.order_date = datetime.datetime.now()
    order.save()
    models.Order.create_order(user=user.id)
    return redirect(url_for("cart"))

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
