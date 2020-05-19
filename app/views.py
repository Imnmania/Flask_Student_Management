from flask import Flask, make_response, request, render_template, url_for, redirect, flash
from .forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from .forms import LoginForm
from app import app


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    #name = "Niloy"

    context = {
        'text': 'This is data by index',
        'name': 'Bob'
    }

    return render_template('index.html', data=context)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        #return 'Form Submitted ..'
        #return ("Submit Successful..")
        if request.form['username'] != 'nb' or request.form['password'] != 'nb':
            flash("Invalid credentials, Please try again!")
        else:
        
            return redirect(url_for('index'))

    return render_template('login.html', title = 'Login Form', form=form)


# @app.route('/user/<name>')
# def user(name):
#     return "<h1> Welcome Mr. {} </h1>".format(name)

# @app.route('/set')
# def setCookie():
#     response = make_response("I have set the cookie")
#     response.set_cookie("myapp", "Flask Web Development")

#     return response

# @app.route('/get')
# def getCookie():
#     myapp = request.cookies.get("myapp")
#     return "Cookie Content is " + str(myapp)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html')
