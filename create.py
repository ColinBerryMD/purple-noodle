# re-initialize the database with a single admin user
from app import db, app
#from models import User, Entry
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    location = db.Column(db.String(500))
    time = db.Column(db.String(100))
with app.app_context():
    db.drop_all()
    db.create_all() 
