from application.database import db
from application.models import User
from flask_security import RegisterForm, LoginForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms import ValidationError

class ExtendedRegisterForm(RegisterForm):
    username = StringField('', [DataRequired()])
    email = StringField('', [DataRequired(),Email()])
    password = PasswordField('',[DataRequired(), Length(min=4)])
    password_confirm = PasswordField('',[DataRequired(), EqualTo('password','Passwords do not match.')])

    def validate_email(self, email):
        try:
            user = db.session.query(User).filter(User.email == email.data).one()
            if user:
                raise ValidationError(email.data+' is already associated with an account.')
        except:
            pass

class CustomLoginForm(LoginForm):
    email = StringField('',[DataRequired(),Email()])
    password = PasswordField('',[DataRequired()])
