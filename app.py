from flask import Flask, make_response, request, render_template, url_for, redirect, flash, render_template_string
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


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# code for models
class UserInfo(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    roles = db.Column(db.String(50), default = 'Student')

    
    #manager = Manager(app)
    #manager.add_command('db', MigrateCommand)

    # def __init__(self, username, password, email):
    #     self.username = username
    #     self.password = password
    #     self.email = email

@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user_info.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

# Setup Flask-User and specify the User data-model
# user_manager = UserManager(app, db, UserInfo)

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
    data = current_user.roles
    return render_template('index.html', name=name, data=data)

@app.route('/base0')
def base0():
    data = current_user.roles
    return data

@app.route('/about')
@login_required
def about():
    data = current_user.roles
    return render_template('about.html', data=data)

@app.route('/contact')
@login_required
def contact():
    data = current_user.roles
    return render_template('contact.html', data=data)

def roleControl():
    # form = LoginForm()
    # user = UserInfo.query.filter_by(username = form.username.data).first()
    return current_user.roles


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            user = UserInfo.query.filter_by(username = form.username.data).first()

            if user:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    #role = user.roles
                    #return (roleControl())

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
@login_required
def register():
    form = RegisterForm()
    data = roleControl()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = UserInfo.query.filter_by(username = form.username.data).first()

            if user:
                flash("Username is already taken, Try another one!")
            else:

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

    # if form.validate_on_submit():
    #     hashed_password = generate_password_hash(form.password.data, method='sha256')

    #     username = form.username.data
    #     # password = form.password.data
    #     password = hashed_password
    #     email = form.email.data

    #     new_register = UserInfo(username=username, password=password, email=email )

    #     db.session.add(new_register)
    #     db.session.commit()

    #     flash("Registration Successful!")

    #     return redirect(url_for('login'))

    return render_template('register.html', form=form, data=data)



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