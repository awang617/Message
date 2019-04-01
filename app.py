
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
                # update the user's plants with new days till_next_water
                return redirect(url_for('profile'))
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
        login_user(user)
        # redirect user to index
        return redirect(url_for('profile'))
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
    return render_template("shop.html")

@app.route('/cart', methods=["GET"])
@login_required
def cart():
    return render_template("cart.html")

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
