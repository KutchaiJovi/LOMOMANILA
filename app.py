from flask import Flask, render_template, request, session, redirect, url_for, make_response, flash, abort
from models import db
from models import User
from models import SignupNext
from models import Post
from models import Comment

# from flask_migrate import Migrate, MigrateCommand

from routes.auth import auth
import datetime
now = datetime.datetime.now()

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:secret@database/testdatabase'
                                        #<dialect+driver>://<username>:<password>@ghost/<database>
db.init_app(app)
# migrate = Migrate(app, db)

app.register_blueprint(auth)
app.url_map.strict_slashes = False

app.secret_key = 'lomomanila'

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

# STATIC PAGES #
@app.route('/')
def index():
    if 'username' in session :
        return redirect(url_for('home'))
    return render_template('index.html', value=0)

@app.route('/about')
def about():
    return render_template('about.html', value=0)

@app.route('/login', methods=['POST', 'GET'])
def loginForm():

    if request.method == 'GET' :
        return render_template('login.html', value=0)
    if request.method == 'POST' :
        session['username'] = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=session['username'], pword=password).first() #filter results ; .all() -return all tasks
        if not user:
            return render_template('login.html', test=2, value=0)
        return redirect(url_for('home'))
    return render_template('login.html', value=0)

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
        # exists = db.session.query(db.session.query(User).filter_by(username=newUser).exists()).scalar()
        checkUser = User.query.filter_by(username=newUser).first()
        if newUser != checkUser :
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
        return render_template('signup.html', value=0, check=True)
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
    return redirect(url_for('profile'))

#PROFILE PAGE
@app.route('/profile')
def userProfile():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        new = SignupNext.query.filter_by(id=user.id).first()
        return render_template('profile.html', users=user, new=new, value=1)
    abort(404)

#HOMEPAGE
@app.route('/dashboard')
def home():
    if 'username' in session :
        user = User.query.filter_by(username=session['username']).first()
        new = SignupNext.query.filter_by(id=user.id).first()
        return render_template('home.html', users=user, new=new, value=1)
    abort(404)

@app.route('/post', methods=['POST'])
def userPost():
    if 'username' in session and 'lomoPhoto' in request.files :
        user = User()
        newPost = Post()

        newPost.post = request.form['userPost']
        newPost.image = request.files['lomoPhoto']
        newPost.filmCam = request.form['cam']
        newPost.filmRoll = request.form['film']
        newPost.postDate = now.strftime("%Y-%m-%d %H:%M")

        db.session.add(newPost)
        # newPost.store()
        flash("Photo saved.")
        db.session.commit()
        return render_template('home.html', value=1, users=user, newPost=newPost)

#ERROR PAGE
@app.errorhandler(404)
def page_not_found(error):
    if 'username' in session:
        return render_template('error.html', value=1), 404
    return render_template('error.html', value=0), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)