import flask_sqlalchemy

db = flask_sqlalchemy.SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    bdate = db.Column(db.DateTime)
    email = db.Column(db.String(100), nullable=False)
    pword = db.Column(db.String(100), nullable=False)
    ig = db.Column(db.String(50), nullable=False)

class SignupNext(db.Model):
    __tablename__ = 'signupNext'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(1000), nullable=False)
    favecam = db.Column(db.String(100), nullable=False)
    faveroll = db.Column(db.String(100), nullable=False)
    favesubject = db.Column(db.String(200), nullable=False)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.LargeBinary)
    filmCam = db.Column(db.String(100))
    filmRoll = db.Column(db.String(100))
    postDate = db.Column(db.DateTime)
    del_post = db.Column(db.Boolean, nullable=False, default=False)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500), nullable=False)
    commentDate = db.Column(db.DateTime)
    del_comment = db.Column(db.Boolean, nullable=False, default=False)