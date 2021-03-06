from flask import Flask, render_template, request, session, redirect, url_for, flash, abort
from models import db, User, SignupNext, Post, Comment, ProfilePicture
from flask_login import LoginManager, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


from routes.auth import auth
import datetime
import os
now = datetime.datetime.now()

from werkzeug.utils import secure_filename
UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:secret@database/testdatabase'
                                        #<dialect+driver>://<username>:<password>@ghost/<database>
db.init_app(app)

app.register_blueprint(auth)
app.url_map.strict_slashes = False

app.secret_key = 'lomomanila'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# EMAIL #
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '201601140@iacademy.edu.ph'
app.config['MAIL_PASSWORD'] = '272829turkey'
app.config['MAIL_DEFAULT_SENDER'] = '201601140@iacademy.edu.ph'
mail = Mail(app)

# LOG IN MANAGER #
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# IMAGE - FILENAME #
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# UPDATES #
@app.route('/avatar', methods=['POST'])
def newAvatar():

    if 'username' in session :
        user = User.query.filter_by(username=session['username']).first()
        userID = user.id

        avatar = ProfilePicture()
        avatar.pic_id = userID
        profilepic = request.files['profilePic']
        filename = secure_filename(profilepic.filename)
        profilepic.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/pic', filename))
        avatar.picpath = os.path.join(app.config['UPLOAD_FOLDER'] + '/pic', filename)

        avatar.picpath = avatar.picpath
        db.session.add(avatar)
        db.session.commit()
        return redirect(url_for('userProfile'))
    abort(404)

@app.route('/avatar/<id>', methods=['POST'])
def avatar(id):

    if 'username' in session :
        user = User.query.filter_by(username=session['username']).first()
        userID = user.id
        
        avatar = ProfilePicture.query.get(id)

        avatar.pic_id = userID
        profilepic = request.files['profilePic']
        filename = secure_filename(profilepic.filename)
        profilepic.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/pic', filename))
        avatar.picpath = os.path.join(app.config['UPLOAD_FOLDER'] + '/pic', filename)

        avatar.picpath = avatar.picpath
        db.session.add(avatar)
        db.session.commit()
        return redirect(url_for('userProfile'))
    abort(404)

@app.route('/update/<id>', methods=['POST'])
def profile_update(id):

    if 'username' in session :

        update = SignupNext.query.get(id) #pass id together with submit

        update.description = request.form['editDesc']
        update.favecam = request.form['editCam']
        update.faveroll = request.form['editRoll']
        update.favesubject = request.form['editSub']

        updateIG = User.query.get(id)
        updateIG.ig = request.form['editIG']
        
        db.session.add(update, updateIG)
        db.session.commit()
        
        return redirect(url_for('userProfile'))
    abort(404)

@app.route('/settings/<id>', methods=['POST'])
def settings(id):

    if 'username' in session :
        settings = User.query.get(id)
        settings.username = request.form['editusername']
        settings.fname = request.form['editfname']
        settings.lname = request.form['editlname']
        settings.gender = request.form['editgender']
        settings.bdate = request.form['editbdate']
        settings.pword = request.form['editpword']

        db.session.add(settings)
        db.session.commit()

        return redirect(url_for('home'))
    abort(404)

# STATIC PAGES #
@app.route('/')
def index():
    if 'username' in session :
        return redirect(url_for('home'))
    session.clear()
    return render_template('index.html', value=0)

@app.route('/about')
def about():
    if 'username' in session:
        return render_template('about.html', value=1)
    return render_template('about.html', value=0)

# PROFILE PAGE #
@app.route('/profile/<id>', methods=['GET'])
def otherProfile(id):
    if 'username' in session:
        user = User.query.get(id)
        new = SignupNext.query.filter_by(id=user.id).first()
        newPost = Post.query.filter_by(users_id=user.id).all()
        
        if not newPost :
            return render_template('profile.html', users=user, new=new, value=1, newPost=0)
        return render_template('profile.html', users=user, new=new, value=1, newPost=newPost, view=1)
    abort(404)

@app.route('/profile')
def userProfile():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        new = SignupNext.query.filter_by(id=user.id).first()
        newPost = Post.query.filter_by(users_id=user.id).all()

        if not newPost :
            return render_template('profile.html', users=user, new=new, value=1, newPost=0, avatar=avatar)
        return render_template('profile.html', users=user, new=new, value=1, newPost=newPost, avatar=avatar)
    abort(404)

# HOMEPAGE #
@app.route('/dashboard')
def home():
    if 'username' in session :
        user = User.query.filter_by(username=session['username']).first()
        new = SignupNext.query.filter_by(id=user.id).first()
        newPost = Post.query.all()

        if not newPost :
            return render_template('home.html', users=user, new=new, value=1, newPost=0, avatar=avatar)
        return render_template('home.html', users=user, new=new, value=1, newPost=newPost, avatar=avatar)
    abort(404)

# POSTS #
@app.route('/post', methods=['POST'])
def userPost():
    if 'username' in session and 'lomoPhoto' in request.files :
        user = User.query.filter_by(username=session['username']).first()
        userID = user.id

        newPost = Post()

        newPost.post = request.form['userPost']
        image = request.files['lomoPhoto']
        newPost.filmCam = request.form['cam']
        newPost.filmRoll = request.form['film']
        newPost.postDate = now.strftime("%Y-%m-%d %H:%M")
        newPost.users_id = userID

        avatarID = ProfilePicture.query.filter_by(pic_id=userID).first()
        newPost.avatar_id = avatarID.id

        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER']+ '/img', filename))
        newPost.imagepath = os.path.join(app.config['UPLOAD_FOLDER']+ '/img', filename)
        
        db.session.add(newPost)
        db.session.commit()

        flash('Your post is now live!')
        return redirect(url_for('home'))
    abort(404)

@app.route('/delete_post/<id>')
def delete_post(id):
    if 'username' in session:
        post = Post.query.get(id)
        
        delete_comment(id)
        db.session.delete(post)
        db.session.commit()
        
        return redirect(url_for('userProfile'))
    abort(404)

@app.route('/delete_comment/<id>')
def delete_comment(id):
    if 'username' in session:
        deleteComment = Comment.query.get(id)
        db.session.delete(deleteComment)
        db.session.commit()
        
        return redirect(url_for('home'))
    abort(404)

@app.route('/delete_commentPost/<id>')
def delete_commentPost(id):
    if 'username' in session:
        delete_comment(id)
        return redirect(url_for('userProfile'))
    abort(404)

@app.route('/comment/<id>', methods=['POST'])
def comment_post(id):
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        userID = user.id
        
        users_post = Post.query.filter_by(id=id).first()
        if users_post :

            reply = Comment()
            
            reply.comment = request.form['comment']
            reply.user_id = userID
            reply.post_id = request.form['postID']

            db.session.add(reply)
            db.session.commit()
            return redirect(url_for('home'))
    abort(404)

#ERROR PAGE
@app.errorhandler(404)
def page_not_found(error):
    if 'username' in session:
        return render_template('error.html', value=1), 404
    return render_template('login.html', value=0, error=True), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)