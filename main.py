from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_simple_geoip import SimpleGeoIP
from app import app, db, Entry

main = Blueprint('main', __name__)

simple_geoip = SimpleGeoIP(app)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    # Retrieve geoip data for the given requester
    geoip_data = simple_geoip.get_geoip_data()

    #return jsonify(data=geoip_data)
    return render_template("profile.html",name=current_user.name, data=geoip_data)

