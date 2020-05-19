from flask import Flask, make_response, request, render_template, url_for, redirect, flash
from .forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from config import Config
from app import views


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)


# manager = Manager(app)

# manager.add_command('db', MigrateCommand)