from flask import Flask, Blueprint, render_template,url_for, redirect, request,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from auth.forms import RegistrationForm
from models import db
from models import User
from datetime import datetime

authen = Blueprint('authen ', __name__)


#mail
app = Flask (__name__)
from flask_mail import Mail
from flask_mail import Message
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'BERNARDINO12'
app.config['UPLOAD_FOLDER'] = './appdata/'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '201601103@iacademy.edu.ph'
app.config['MAIL_PASSWORD'] = app.secret_key
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
db = SQLAlchemy(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@authen.route('/sandbox')
def send_email(in_subject, in_emailaddress, in_username, in_content):
	msg = Message(in_subject,
				sender="201601103@iacademy.edu.ph",
				recipients=["201601103@iacademy.edu.ph"])
	msg.html = render_template('email.html',username=in_username,content=in_content)
	mail.send(msg)
	return 'OK'




@authen.route('/login')
def login():

    if current_user.is_authenticated:
        flash('You are aldready Signed In')
        return redirect(url_for('main.profile')) 

    return render_template('login.html')

@authen.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # check if meron user na ganon
    user = User.query.filter_by(username=username).first()

    
    # Check password na naka hash
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('authen .login')) # Error if no user or wrong credentials

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

#last seen user
@authen.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@authen.route('/signup')
def signup():
    return render_template('/signup.html')

@authen.route('/signup', methods=['GET', 'POST'])
def signup_post():
    email = request.form.get('email')
    instagram_account = request.form.get('instagram')
    username = request.form.get('username')
    password = request.form.get('password')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('authen .signup'))

    new_user = User(username=username, fname=fname, lname=lname, email=email, instagram_account=instagram_account,password=generate_password_hash(password,method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    send_email("Welcome to LOMOMANILA!", email, username, "Thank you for registering! LOMON!")
    return redirect(url_for('authen .login'))



@authen.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))