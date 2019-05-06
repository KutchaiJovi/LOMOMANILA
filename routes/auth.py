from flask import Blueprint, render_template, request, redirect
from lib.validators.signup_validator import signupValidator

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login')
def login_form():
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signUp_form():
    if request.method == 'GET':
        username = request.cookies.get('username')
        return render_template('signup.html')
    else:
        data = {'name' : request.form('name'), 'email' : request.form('email'),
        'pword' : request.form('password')} #dictionary
        signupValidator = signupValidator(data)
    return render_template('signup.html')


#Methods:
#def  __init__ (self, name):
#   self.<property name> = value

#def run (self, parameter1):
#   print ('run')

#obj.run(parameter1)