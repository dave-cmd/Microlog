from app.model import People
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError,Length

from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember_me'))
    submit = SubmitField(_l('Sign In'))
    
class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'),validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))
    
    def validate_username(self, username):
        user = People.query.filter(People.username ==username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    def validate_email(self, email):
        mail  = People.query.filter(People.email==email.data).first()
        if mail is not None:
            raise ValidationError('Please use a different email address')
            
class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    about_me = TextAreaField(_l('About Me'), validators=[Length(min=0, max=150)])
    picture = FileField(_l('Picture'), validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField(_l('Submit'))
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = People.query.filter(People.username == username.data).first()
            print(user)
            
            if user:
                raise ValidationError(_l("Please use a different username."))
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = People.query.filter(People.email == email.data).first()
            
            if user:
                raise ValidationError(_l("Please use a different email address."))
                
                
class EmptyForm(FlaskForm):
    submit = SubmitField(_l('Submit'))
    
class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something...'), validators=[DataRequired(), Length(min=0,max=150)]) 
    submit = SubmitField(_l('Submit'))
    
class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(),Email()]) 
    submit = SubmitField(_l('Request Password Reset'))
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))
    
    
    
    
    