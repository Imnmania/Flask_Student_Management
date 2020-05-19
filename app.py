from flask import Flask, make_response, request, render_template, url_for, redirect, flash
from form import LoginForm, RegisterForm
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager
from flask_login import login_user, logout_user, current_user, login_required
from flask_login import UserMixin

# code for init
app = Flask(__name__)

app.config['SECRET_KEY'] = '6f430236b96d75aa5c3708d15ddcf345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://demo:password@localhost/crud'    #dbSysName://user:password@host/dbname
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

#manager = Manager(app)
#manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# code for models
class UserInfo(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))


    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))

# code for views
@app.route('/')
@app.route('/home')
@app.route('/index')
@login_required
def index():
    #name = "Niloy"

    # context = {
    #     'text': 'This is data by index',
    #     'name': 'Bob'
    # }

    name = current_user.username

    return render_template('index.html', name=name)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            user = UserInfo.query.filter_by(username = form.username.data).first()

            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)

                    return redirect(url_for('index'))

                # flash("Invalid Credentials, Please Try Again!")
        flash("Invalid Credentials, Please Try Again!")
    return render_template('login.html', form=form)

    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
        


@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        username = form.username.data
        # password = form.password.data
        password = hashed_password
        email = form.email.data

        new_register = UserInfo(username=username, password=password, email=email )

        db.session.add(new_register)
        db.session.commit()

        flash("Registration Successful!")

        return redirect(url_for('login'))

    return render_template('register.html', form=form)



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




if __name__ == '__main__':
    app.run(debug=True)
    #manager.run()