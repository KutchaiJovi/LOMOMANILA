from flask import Flask, render_template, request, session, redirect, url_for, make_response, flash, abort
from models import db
from models import User
from models import SignupNext
from models import Post
from models import Comment
from models import ProfilePicture

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

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# DATABASE #
@app.route('/test-connection')
def hello():
    try:
        db.session.query('1').all()
        return 'Connected.'
    except Exception as e:
        return str(e)

@app.route('/create-schema')
def create_schema():
    db.create_all()
    return 'Schema created.'

# UPDATE #

@app.route('/avatar/<id>', methods=['POST'])
def avatar(id):

    if 'username' in session :
        user = User.query.filter_by(username=session['username']).first()
        userID = user.id

        avatar = ProfilePicture()

        profilepic = request.files['profilePic']
        avatar.pic_id = userID
        filename = secure_filename(profilepic.filename)
        profilepic.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/pic', filename))
        avatar.picpath = os.path.join(app.config['UPLOAD_FOLDER'] + '/pic', filename)
        
        db.session.add(avatar)
        db.session.commit()
        
        return redirect(url_for('userProfile'))

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

# STATIC PAGES #
@app.route('/')
def index():
    if 'username' in session :
        return redirect(url_for('home'))
    session.clear()
    return render_template('index.html', value=0)

@app.route('/about')
def about():
    return render_template('about.html', value=0)

@app.route('/login', methods=['POST', 'GET'])
def loginForm():

    if request.method == 'GET' :
        return render_template('login.html', value=0)
    elif request.method == 'POST' :
        session['username'] = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=session['username'], pword=password).first() #filter results ; .all() -return all tasks
        if not user:
            session.clear()
            return render_template('login.html', test=2, value=0)
        return redirect(url_for('home'))
    return render_template('login.html', value=0)

@app.route('/reset')
def reset():
    return render_template('resetPassword.html', value=0)

@app.route('/resetpassword', methods=['POST'])
def resetpassword():

    if request.method == 'POST' :
        pword = request.form['newpword']
        confpword = request.form['confpword']
        update = User.query.filter_by(email=request.form['email']).first()
        if update:
            if confpword != pword :
                return  render_template('resetPassword.html', value=0, check=2)
            else :
                update.pword = request.form['newpword']

                db.session.add(update)
                db.session.commit()
                return redirect(url_for('loginForm'))
        return render_template('resetPassword.html', value=0, test=3)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/lomoOn')
def lomoOn():
    return render_template('signup.html', value=0)

@app.route('/signup', methods=['POST'])
def signUp():

    if request.method == 'POST' :
        users = User()
        newUser = request.form['username']
        checkUser = User.query.filter_by(username=newUser).first()
        if not checkUser:
            users.username = newUser
            users.fname = request.form['firstName']
            users.lname = request.form['lastName']
            users.gender = request.form['gender']
            users.bdate = request.form['bdate']
            users.ig = request.form['igUsername']
            users.email = request.form['email']

            session['username'] = users.username
            password = request.form['password']
            users.pword = password
            confPassword = request.form['confPassword']

            if password != confPassword :
                return render_template('signup.html', test=2, value=0)
            else :
                db.session.add(users)
                db.session.commit()
                return render_template('signup.html', value=1, sign=1)
        return render_template('signup.html', value=0, check=1 , sign=0)
    return redirect(url_for('lomoOn'))

@app.route('/signup-next', methods=['POST'])
def signUpNext():

    new = SignupNext()

    new.description = request.form['description']
    new.favecam = request.form['favecam']
    new.faveroll = request.form['faveroll']
    new.favesubject = request.form['favesubject']

    db.session.add(new)
    db.session.commit()
    return redirect(url_for('userProfile'))

#PROFILE PAGE
@app.route('/profile')
def userProfile():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        new = SignupNext.query.filter_by(id=user.id).first()
        newPost = Post.query.filter_by(users_id=user.id).all()
        avatar = ProfilePicture.query.filter_by(pic_id=user.id).all()

        if not newPost :
            return render_template('profile.html', users=user, new=new, value=1, newPost=0, avatar=avatar)
        return render_template('profile.html', users=user, new=new, value=1, newPost=newPost, avatar=avatar)
    abort(404)

#HOMEPAGE
@app.route('/dashboard')
def home():
    if 'username' in session :
        user = User.query.filter_by(username=session['username']).first()
        new = SignupNext.query.filter_by(id=user.id).first()
        newPost = Post.query.filter_by(users_id=user.id).all()
        avatar = ProfilePicture.query.filter_by(pic_id=user.id).all()
        # rep = Comment.query.filter_by(rep_id=user.id).all()
        if not newPost :
            return render_template('home.html', users=user, new=new, value=1, newPost=0, avatar=avatar)
        return render_template('home.html', users=user, new=new, value=1, newPost=newPost, avatar=avatar)
    abort(404)



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

        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER']+ '/img', filename))
        newPost.imagepath = os.path.join(app.config['UPLOAD_FOLDER']+ '/img', filename)
        
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for('home'))

@app.route('/delete_post/<id>')
def delete_post(id):
    post = Post.query.get(id) # shortcut for Task.query.filter_by(id=1).first
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/comment', methods=['POST'])
def comment_post():
    reply = Comment()
    reply.comment = request.form['comment']
    db.session.add(reply)
    db.session.commit()
    return redirect(url_for('home'))

#ERROR PAGE
@app.errorhandler(404)
def page_not_found(error):
    if 'username' in session:
        return render_template('error.html', value=1), 404
    return render_template('error.html', value=0), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)