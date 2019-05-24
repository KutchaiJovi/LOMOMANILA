from flask import Flask, render_template, request, session, redirect, url_for, make_response, flash, abort
# from auth.forms import RegistrationForm
from models import db


import os


from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()

app = Flask (__name__)
#secret key
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:secret@database/testdatabase'
                                        #<dialect+driver>://<username>:<password>@ghost/<database>
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'authen .login'
login_manager.init_app(app)





from models import User

#Creates cookie and searches it in db from id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




#auth is for login sign 
from blueprints.authen import authen as authen_blueprint
app.register_blueprint(authen_blueprint)

#main will be index and profile
from blueprints.main import main as main_blueprint
app.register_blueprint(main_blueprint)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
