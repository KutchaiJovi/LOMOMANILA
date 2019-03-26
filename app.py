from flask import Flask, render_template, request, session, escape, redirect, url_for, make_response
#render_template -- jinja2 statements

app = Flask (__name__)

app.secret_key = 'babajigabajulaba'

@app.route('/')
def hello():
    return 'Hello, World!'

#@app.route('/hello/<name>')
#def hello_name(name):
#    return "Hello, %s" % name
#http://my-flask-app.com:5000/hello/kutch

@app.route('/hello/<name>')
def hello_name(name):
    return render_template('hello.html', name=name)

@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login_form.html')

@app.route('/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    return "Email: %s <br> Password: %s" % (email, password)

# HOMEWORK #
# @app.route ('/')
# def index():
#     if 'email' in session:
#         #return 'Logged in as %s' %escape(session['email'])
#         return redirect(url_for('/loginForm'))
#     return 'You are not logged in.'
@app.route ('/my-profile')
def profile():
    if 'username' in session:
        resp = make_response(render_template('success.html', email=session['username'], password=session['password'], username = request.cookies.get('username')))
        resp.set_cookie('username', 'the username')
        return resp
    return redirect(url_for('login_form1'))

@app.route('/loginForm', methods=['GET', 'POST'])
def login_form1():

    if request.method == 'GET':
        username = request.cookies.get('username')
        return render_template('loginForm_HO_Viray.html')
    else:
        email = request.form['email']
        password1 = request.form['password']

        # resp = make_response(render_template('success.html'))

        if email == 'test@flask.app' and password1 == 'password123':
            session['username'] = request.form['email']
            session['password'] = request.form['password']
            return redirect(url_for('profile'))
        return render_template('loginForm_HO_Viray.html', value=2)

@app.route ('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_form1'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)