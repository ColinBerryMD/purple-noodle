# re-initialize the database with a single admin user
from app import db, app
from models import User, Entry

with app.app_context():
    db.drop_all()
    db.create_all() 
