from flask_login import login_required, current_user
from flask import Blueprint, render_template, url_for, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from auth.forms import RegistrationForm
from models import db
from models import User, Post, Comment
from flask import Flask
from flask_moment import Moment

app = Flask (__name__)

main = Blueprint('main', __name__)
moment = Moment(app)

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
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
@main.route('/sandbox')
def send_email(in_subject, in_emailaddress, in_username, in_content):
	msg = Message(in_subject,
				ssender="bot@asamplesiteforum.com",
				recipients=["201501330iacademy.edu.ph"])
	msg.html = render_template('email.html',username=in_username,content=in_content)
	mail.send(msg)
	return 'OK'





@main.route('/index')
@main.route('/')
def index():

    return render_template('index.html')



@main.route('/home')
@login_required
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    comments = Comment.query.order_by(Comment.timestamp.desc()).all()
    
    len_posts = len(posts)
    
    return render_template('home.html', title='Home', comments=comments, posts=posts, len_posts = len_posts, user_id = current_user.id
                                                    , fname=current_user.fname, lname=current_user.lname,username=current_user.username, about_me=current_user.about_me, favecam=current_user.favecam, faveroll = current_user.faveroll, favesubject=current_user.favesubject, instagram_account=current_user.instagram_account)





@main.route('/home', methods=['GET', 'POST'])
@login_required
def home_post():
    email = current_user.email
    username = current_user.username
    post = Post(
                author = current_user ,
                body = request.form.get("userPost") ,
                used_cam = request.form.get('used_cam') ,
                used_roll = request.form.get('used_roll')
                )
    db.session.add(post)
    db.session.commit()
    send_email("Your post is now live in LOMOMANILA!", email, username, "Post is now live. Thank you! LOMON!")

    flash('Your post is now live!')
    return redirect(url_for('main.home'))

@main.route('/comment', methods=['GET', 'POST'])
@login_required
def home_comment():
    comment = Comment(
                post_id = request.form.get("post"),
                commentor = current_user,
                body = request.form.get("body")
                )
    db.session.add(comment)
    db.session.commit()

    return redirect(url_for('main.home'))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', fname=current_user.fname, email=current_user.email, lname=current_user.lname, username=current_user.username, about_me=current_user.about_me, favecam=current_user.favecam, faveroll = current_user.faveroll, favesubject=current_user.favesubject, instagram_account = current_user.instagram_account)

#create schema db
@main.route('/create-schema')
def create_schema():
    db.create_all()
    return 'Schema created.'

@main.route('/editprofile')
@login_required
def editprofile():
    return render_template('/editprofile.html', fname=current_user.fname, lname=current_user.lname,username=current_user.username, about_me=current_user.about_me, favecam=current_user.favecam, faveroll = current_user.faveroll, favesubject=current_user.favesubject, instagram_account=current_user.instagram_account)

@main.route('/editprofile', methods=['GET', 'POST'])
@login_required
def editprofile_post():
    current_user.about_me = request.form.get('about_me')
    current_user.favecam = request.form.get('favecam')
    current_user.faveroll = request.form.get('faveroll')
    current_user.favesubject = request.form.get('favesubj')
    current_user.instagram_accout = request.form.get('instagram_account')
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('main.profile'))


@main.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Post.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)

    
    
