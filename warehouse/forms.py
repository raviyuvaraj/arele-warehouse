from warehouse import db,User
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,Email,EqualTo,DataRequired,ValidationError

class RegisterForm(FlaskForm):
    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists')
        # return super().validate(extra_validators)
    first_name = StringField(label='First Name',validators=[Length(min=3,max=30),DataRequired()])
    last_name = StringField(label='Last Name')
    email = StringField(label='E-mail',validators=[Email(),DataRequired()])
    password = PasswordField(label='Password:',validators=[Length(min=6),DataRequired()])
    confirm_password = PasswordField(label='Confirm Password:',validators=[EqualTo('password'),DataRequired()])
    submit = SubmitField(label='Sign Up')

class LoginForm(FlaskForm):
    email = StringField(label='E-mail',validators=[Email(),DataRequired()])
    password = PasswordField(label='Password:',validators=[DataRequired()])
    submit = SubmitField(label='Login')


class MoveItemForm(FlaskForm):
    submit = SubmitField(label='Move Item')

class ReturnItemForm(FlaskForm):
    submit = SubmitField(label='Return Item')