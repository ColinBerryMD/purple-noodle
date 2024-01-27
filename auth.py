from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt, User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods= ( 'GET','POST'))
def login():
    if request.method == 'POST':

    # login code goes here 
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        try:
            user = User.query.filter_by(email=email).one()
        except:
            flash('User not found.')
            return render_template('login.html')  # if the user doesn't exist or password is wrong, reload the page 

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not bcrypt.check_password_hash( user.password, password ):
            flash('Please check your login details and try again.')
            return render_template('login.html')  # if the user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

    # GET request
    return render_template('login.html')

@auth.route('/signup', methods= ('GET','POST'))
def signup():

    if request.method == 'POST':
    # code to validate and add user to database goes here
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('That email is already registered.')
            return redirect(url_for('auth.signup'))
        
        if not ( password == confirm ):
            flash('Passwords must match.')
            return redirect(url_for('auth.signup')) 

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        hash = bcrypt.generate_password_hash(password)
        new_user = User(email=email, name=name, password=hash)
        
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
                
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth.route('/new_password', methods= ('GET','POST'))
@login_required
def new_password():

    if request.method == 'POST':
    # code to validate and add user to database goes here
        password = request.form.get('password')
        newpassword = request.form.get('newpassword')
        confirm = request.form.get('confirm')
        
        if not ( newpassword == confirm ):
            flash('Passwords must match.')
            return redirect(url_for('auth.new_password')) 

        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not bcrypt.check_password_hash( current_user.password, password ):
            flash('Need original password to change it.')
            return render_template('new_password.html')  # if the user doesn't exist or password is wrong, reload the page

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        hash = bcrypt.generate_password_hash(password)
        update_user = User.query.filter_by(id=current_user.id).one()
        
        # add the new user to the database
        update_user.password=hash
        db.session.commit()
                
        return redirect(url_for('main.index'))

    return render_template('new_password.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
