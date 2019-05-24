from wtforms import Form, BooleanField, StringField, PasswordField, validators

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    instagram_account = StringField('Instagram Account', [validators.DataRequired()])


# class LoginForm(Form):
#     username = StringField(_l('Username'), validators=[DataRequired()])
#     password = PasswordField(_l('Password'), validators=[DataRequired()])
#     submit = SubmitField(_l('Sign In'))

# class checkPassword():
#     password = 