from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import User
   
app = Flask(__name__)  


#app.config['SECRET_KEY'] = environ['WTF_SECRET']
app.config['SECRET_KEY'] = 'not_very_secret_key'

# uncomment this to use SQLite for development
#basedir = os.path.abspath(os.path.dirname(__file__))
#db_url = 'sqlite:///' + os.path.join(basedir, 'database.db')

# uncomment this to use original 'sms' database
#db_password = environ.get('MYSQL_WEBSERVER_PASSWORD')
#db_url = 'mysql+pymysql://webserver:'+db_password+'@localhost/sms'

# uncomment this to use mysql for with unprivileged account
db_password = environ.get('MYSQL_WEBSERVER_PASSWORD')
db_url = 'mysql+pymysql://webserver:'+db_password+'@localhost/purple_noodle'

# uncomment this to use mysql and modify 'fluffy-waffle' database
#db_password = environ.get('MYSQL_PRIVILEGED_PASSWORD')
#db_url = 'mysql+pymysql://privileged:'+db_password+'@localhost/purple_noodle'

app.config['SQLALCHEMY_DATABASE_URI'] = db_url

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


db.init_app(app)

# blueprint for auth routes in our app
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from main import main as main_blueprint
app.register_blueprint(main_blueprint)
