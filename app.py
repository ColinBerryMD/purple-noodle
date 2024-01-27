from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for 
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv, find_dotenv
   
app = Flask(__name__)  
load_dotenv(find_dotenv())


app.config['SECRET_KEY'] = environ['WTF_SECRET']
#app.config['SECRET_KEY'] = 'not_very_secret_key'

# uncomment this to use SQLite for development
#basedir = os.path.abspath(os.path.dirname(__file__))
#db_url = 'sqlite:///' + os.path.join(basedir, 'database.db')

# uncomment this to use original 'sms' database
#db_password = environ.get('MYSQL_WEBSERVER_PASSWORD')
#db_url = 'mysql+pymysql://webserver:'+db_password+'@localhost/sms'

# uncomment this to use mysql for with unprivileged account
#db_password = environ.get('MYSQL_WEBSERVER_PASSWORD')
#db_url = 'mysql+pymysql://webserver:'+db_password+'@localhost/purple_noodle'

# uncomment this to use mysql and modify 'purple_noodle' database
db_password = environ.get('MYSQL_PRIVILEGED_PASSWORD')
db_url = 'mysql+pymysql://privileged:'+db_password+'@localhost/purple_noodle'

app.config['SQLALCHEMY_DATABASE_URI'] = db_url

bcrypt = Bcrypt()

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)    

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    location = db.Column(db.String(500))
    time = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id):
# since the user_id is just the primary key of our user table, use it in the query for the user
	return User.query.get(int(user_id))

# blueprint for auth routes in our app
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from main import main as main_blueprint
app.register_blueprint(main_blueprint)
