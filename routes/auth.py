from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, flash, abort
from models import db, User, SignupNext, Post, Comment, ProfilePicture
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

auth = Blueprint('auth', __name__)
# , url_prefix='/auth'

# EMAIL #
from flask_mail import Message
from app import mail
import smtplib

def send_email(subject, email, username):
	msg = Message(subject,
				sender="201601140@iacademy.edu.ph",
				recipients=["201601140@iacademy.edu.ph"])
	msg.html = render_template('email.html',username=username)
	mail.send(msg)
	return 'OK'

@auth.route('/email')
def email():
    user = User.query.filter_by(username=session['username']).first()
    return render_template('email.html', user=user)

# DATABASE AND CONNECTION #
@auth.route('/test-connection')
def hello():
    try:
        db.session.query('1').all()
        return 'Connected.'
    except Exception as e:
        return str(e)

@auth.route('/create-schema')
def create_schema():
    db.create_all()
    return 'Schema created.'

@auth.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# LOG IN #
@auth.route('/login')
def login():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        new = SignupNext.query.filter_by(id=user.id).first()
        newPost = Post.query.all()
        
        return render_template('home.html', logged=True, users=user, new=new, value=1, newPost=newPost)
    return render_template('login.html', value=0)

@auth.route('/login', methods=['POST'])
def loginForm():

    if request.method == 'POST' :
        session['username'] = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=session['username']).first() #filter results ; .all() -return all tasks
        if not user or not check_password_hash(user.pword, password):
            session.clear()
            return render_template('login.html', test=2, value=0)
        return redirect(url_for('home'))
    return render_template('login.html', value=0)


# LOG OUT #
@auth.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# SIGN UP #
@auth.route('/lomoOn')
def lomoOn():
    return testsignUp()

@auth.route('/signup')
def testsignUp():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        new = SignupNext.query.filter_by(id=user.id).first()
        newPost = Post.query.all()
        avatar = ProfilePicture.query.filter_by(pic_id=user.id).first()
        
        return render_template('home.html', logged=True, users=user, new=new, value=1, newPost=newPost, avatar=avatar)
    return render_template('signup.html', value=0)

@auth.route('/signup', methods=['POST'])
def signUp_post():

    if 'username' in session :
        return render_template('home.html', logged=True)
    elif 'username' not in session and request.method == 'POST' :
        users = User()
        newUser = request.form['username']
        newEmail = request.form['email']
        checkUser = User.query.filter_by(username=newUser).first()
        if not checkUser:
            users.username = newUser
            users.fname = request.form['firstName']
            users.lname = request.form['lastName']
            users.gender = request.form['gender']
            users.bdate = request.form['bdate']
            users.ig = request.form['igUsername']
            users.email = newEmail

            password = request.form['password']
            users.pword = generate_password_hash(password,method='sha256')
            confPassword = request.form['confPassword']

            checkEmail = User.query.filter_by(email=newEmail).first()

            if checkEmail :
                return render_template('signup.html', email=False, value=0)
            elif password != confPassword :
                return render_template('signup.html', test=2, value=0)
            else :
                db.session.add(users)
                db.session.commit()
                session['username'] = users.username

                return render_template('signup.html', value=1, sign=1)
        return render_template('signup.html', value=0, check=1 , sign=0)
    return redirect(url_for('lomoOn'))

@auth.route('/signup-next', methods=['POST'])
def signUpNext():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        userID = user.id

        new = SignupNext()

        new.description = request.form['description']
        new.favecam = request.form['favecam']
        new.faveroll = request.form['faveroll']
        new.favesubject = request.form['favesubject']
        new.users_id = userID

        db.session.add(new)
        db.session.commit()
        return redirect(url_for('userProfile'))
    abort(404)