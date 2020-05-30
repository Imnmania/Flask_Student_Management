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

## UserInfo Table
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


## Admin Table
class Admin(UserMixin, db.Model):
    #__tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key = True)
    admin_name = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
    roles = db.Column(db.String(50), default = 'Admin')


## Student Table
class Student(UserMixin, db.Model):
    #__tablename__ = 'student'
    id = db.Column(db.Integer, primary_key = True)
    student_name = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    status = db.Column(db.String(100))
    cgpa = db.Column(db.String(100))
    dept_id = db.Column(db.Integer)
    major = db.Column(db.String(100))
    date_of_birth = db.Column(db.String(100))
    father_name = db.Column(db.String(100))
    mother_name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    credit_passed = db.Column(db.Integer)
    password = db.Column(db.String(100))
    roles = db.Column(db.String(50), default = 'Student')


## Faculty Table
class Faculty(UserMixin, db.Model):
    #__tablename__ = 'faculty'
    id = db.Column(db.Integer, primary_key = True)
    faculty_name = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(100))
    faculty_init = db.Column(db.String(100))
    phone = db.Column(db.Integer)
    dept_id = db.Column(db.Integer)
    status = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    guardian_name = db.Column(db.String(100))
    marital_status = db.Column(db.String(100))
    salary = db.Column(db.String(100))
    password = db.Column(db.String(100))
    roles = db.Column(db.String(50), default = 'Faculty')

## Course Table
class Course(UserMixin, db.Model):
    course_id = db.Column(db.String(100), primary_key = True)
    course_name = db.Column(db.String(100))
    credit_hr = db.Column(db.Integer)
    dept_id = db.Column(db.Integer)


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

## code for views
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

    # name = current_user.username
    name = current_user
    data = current_user.roles
    return render_template('index.html', name=name, data=data)


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

@app.route('/student_portal', methods = ['GET', 'POST'])
@login_required
def student_portal():
    data = current_user.roles

    if data == 'Admin':
        all_students = Student.query.all()
        return render_template('student_portal.html', data=data, all_students=all_students)
    else:
        return render_template('404.html')


@app.route('/faculty_portal', methods = ['GET', 'POST'])
@login_required
def faculty_portal():
    data = current_user.roles
    
    if data == 'Admin':
        all_faculties = Faculty.query.all()
        return render_template('faculty_portal.html', data=data, all_faculties=all_faculties)
    else:
        return render_template('404.html')


@app.route('/admin_portal', methods = ['GET', 'POST'])
@login_required
def admin_portal():
    data = current_user.roles
    
    if data == 'Admin':
        all_admins = Admin.query.all()
        return render_template('admin_portal.html', data=data, all_admins=all_admins)
    else:
        return render_template('404.html')


@app.route('/course_portal', methods = ['GET', 'POST'])
@login_required
def course_portal():
    data = current_user.roles

    if data == 'Admin':
        all_courses = Course.query.all()
        return render_template('course_portal.html', data=data, all_courses=all_courses)
    else:
        return render_template('404.html')


@app.route('/user_information', methods = ['GET', 'POST'])
@login_required
def user_information():
    data = current_user.roles
    
    if data == 'Student':
        all_data = Student.query.get(current_user.id)
        return render_template('user_information.html', data=data, all_data=all_data)
    
    elif data == 'Faculty':
        all_data = Faculty.query.get(current_user.id)
        return render_template('user_information.html', data=data, all_data=all_data)
    
    else:
        return render_template('404.html')


## Code for Views End



## Login Function
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            user = UserInfo.query.filter_by(username = form.username.data).first()

            if user:
                # if check_password_hash(user.password, form.password.data):
                if (user.password == form.password.data):  
                    login_user(user)
                    #role = user.roles
                    #return (roleControl())
                    # session = user.username

                    return redirect(url_for('index'))

                # flash("Invalid Credentials, Please Try Again!")
        flash("Invalid Credentials, Please Try Again!")
    return render_template('login.html', form=form)

    
## Logout Function    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
        

## Admin Register Function
@app.route('/register', methods = ['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()
    data = roleControl()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = AdminInfo.query.filter_by(admin_name = form.username.data).first()

            if user:
                flash("Username is already taken, Try another one!")
            else:

                # hashed_password = generate_password_hash(form.password.data, method='sha256')

                admin_name = form.username.data
                password = form.password.data
                # password = hashed_password
                email = form.email.data

                new_register = AdminInfo(admin_name=admin_name, password=password, email=email )

                db.session.add(new_register)
                db.session.commit()

                flash("Registration Successful!")

                return redirect(url_for('login'))

    return render_template('register.html', form=form, data=data)

## Admin Register Function (ver2)
@app.route('/ad_insert', methods=['GET','POST'])
def ad_insert():
    if request.method == 'POST':

        try:
            admin_name = request.form['admin_name']
            password = request.form['password']
            email = request.form['email']

            my_data = Admin(admin_name=admin_name, password=password, email=email)


            db.session.add(my_data)
            db.session.commit()

            flash("New Admin Added!")

        except Exception:
            flash("That Admin Already Exists!!!")


        return redirect(url_for('admin_portal'))

## Admin Update Function
@app.route('/ad_update', methods=['GET','POST'])
def ad_update():
    if request.method == 'POST':
        my_data = Admin.query.get(request.form.get('id'))  # this is the hidden id created in index.html

        my_data.admin_name = request.form['admin_name']
        my_data.password = request.form['password']
        my_data.email = request.form['email']


        db.session.commit()
        flash("Admin List Updated!")

        return redirect(url_for('admin_portal'))


## Admin Delete Function
@app.route('/ad_delete/<id>', methods=['GET', 'POST'])
def ad_delete(id):
    my_data = Admin.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash('Admin Deleted Successfully!')

    return redirect(url_for('admin_portal'))


## Student Register Function
@app.route('/st_insert', methods=['GET','POST'])
def st_insert():
    if request.method == 'POST':

        try:
            student_name = request.form['student_name']
            email = request.form['email']
            phone = request.form['phone']
            status = request.form['status']
            cgpa = request.form['cgpa']
            dept_id = request.form['dept_id']
            major = request.form['major']
            date_of_birth = request.form['date_of_birth']
            father_name = request.form['father_name']
            mother_name = request.form['mother_name']
            address = request.form['address']
            credit_passed = request.form['credit_passed']
            password = request.form['password']

            my_data = Student(student_name=student_name, email=email, phone=phone, status=status, cgpa=cgpa, dept_id=dept_id, major=major, date_of_birth=date_of_birth, father_name=father_name,
            mother_name=mother_name, address=address, credit_passed=credit_passed, password=password )


            db.session.add(my_data)
            db.session.commit()

            flash("New Student Added!")

        except Exception:
            flash("That Student Already Exists!!!")


        return redirect(url_for('student_portal'))


## Student Update Function
@app.route('/st_update', methods=['GET','POST'])
def st_update():
    if request.method == 'POST':
        my_data = Student.query.get(request.form.get('id'))  # this is the hidden id created in index.html

        my_data.student_name = request.form['student_name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.status = request.form['status']
        my_data.cgpa = request.form['cgpa']
        my_data.dept_id = request.form['dept_id']
        my_data.major = request.form['major']
        my_data.date_of_birth = request.form['date_of_birth']
        my_data.father_name = request.form['father_name']
        my_data.mother_name = request.form['mother_name']
        my_data.address = request.form['address']
        my_data.credit_passed = request.form['credit_passed']
        my_data.password = request.form['password']


        db.session.commit()
        flash("Student List Updated!")

        return redirect(url_for('student_portal'))


## Student Delete Function
@app.route('/st_delete/<id>', methods=['GET', 'POST'])
def st_delete(id):
    my_data = Student.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash('Student Deleted Successfully!')

    return redirect(url_for('student_portal'))



## Faculty Register Function
@app.route('/fc_insert', methods=['GET','POST'])
def fc_insert():
    if request.method == 'POST':

        try:

            faculty_name = request.form['faculty_name']
            email = request.form['email']
            faculty_init = request.form['faculty_init']
            phone = request.form['phone']
            dept_id = request.form['dept_id']
            status = request.form['status']
            qualification = request.form['qualification']
            guardian_name = request.form['guardian_name']
            marital_status = request.form['marital_status']
            salary = request.form['salary']
            password = request.form['password']
            

            my_data = Faculty(faculty_name=faculty_name, email=email, faculty_init=faculty_init, phone=phone,
            dept_id=dept_id, status=status, qualification=qualification, guardian_name=guardian_name, marital_status=marital_status,
            salary=salary, password=password)


            db.session.add(my_data)
            db.session.commit()

            flash("New Faculty Added!")

        except Exception:
            flash("Faculty Already Exists!!!")
        

        return redirect(url_for('faculty_portal'))


## Faculty Update Function
@app.route('/fc_update', methods=['GET','POST'])
def fc_update():
    if request.method == 'POST':
        my_data = Faculty.query.get(request.form.get('id'))  # this is the hidden id created in index.html

        my_data.faculty_name = request.form['faculty_name']
        my_data.email = request.form['email']
        my_data.faculty_init = request.form['faculty_init']
        my_data.phone = request.form['phone']
        my_data.dept_id = request.form['dept_id']
        my_data.status = request.form['status']
        my_data.qualification = request.form['qualification']
        my_data.guardian_name = request.form['guardian_name']
        my_data.marital_status = request.form['marital_status']
        my_data.salary = request.form['salary']
        my_data.password = request.form['password']


        db.session.commit()
        flash("Faculty List Updated!")

        return redirect(url_for('faculty_portal'))


## Faculty Delete Function
@app.route('/fc_delete/<id>', methods=['GET', 'POST'])
def fc_delete(id):
    my_data = Faculty.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash('Faculty Deleted Successfully!')

    return redirect(url_for('faculty_portal'))


## Course Insert Function
@app.route('/cor_insert', methods=['GET','POST'])
def cor_insert():
    if request.method == 'POST':

        try:
            course_id = request.form['course_id']
            course_name = request.form['course_name']
            credit_hr = request.form['credit_hr']
            dept_id = request.form['dept_id']

            my_data = Course(course_id=course_id, course_name=course_name, credit_hr=credit_hr, dept_id=dept_id)


            db.session.add(my_data)
            db.session.commit()

            flash("New Course Added!")

        except Exception:
            flash("That Course Already Exists!!!")


        return redirect(url_for('course_portal'))


## Course Update Function
@app.route('/cor_update', methods=['GET','POST'])
def cor_update():
    if request.method == 'POST':
        my_data = Course.query.get(request.form.get('course_id'))  # this is the hidden id

        my_data.course_id = request.form['course_id']
        my_data.course_name = request.form['course_name']
        my_data.credit_hr = request.form['credit_hr']
        my_data.dept_id = request.form['dept_id']


        db.session.commit()
        flash("Course List Updated!")

        return redirect(url_for('course_portal'))


## Course Delete Function
@app.route('/cor_delete/<course_id>', methods=['GET', 'POST'])
def cor_delete(course_id):
    my_data = Course.query.get(course_id)
    db.session.delete(my_data)
    db.session.commit()
    flash('Course Deleted Successfully!')

    return redirect(url_for('course_portal'))

# # Cookie Management
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

@app.route('/base0')
def base0():
    data = current_user.roles
    return data

@app.route('/base1')
def base1():
    data = current_user.roles
    return data

def roleControl():
    # form = LoginForm()
    # user = UserInfo.query.filter_by(username = form.username.data).first()
    return current_user.roles



if __name__ == '__main__':
    app.run(debug=True)
    #manager.run()