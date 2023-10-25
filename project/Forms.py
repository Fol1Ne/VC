from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileRequired


class LoginForm(FlaskForm):
    login = StringField("Login: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators={DataRequired()})
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    login = StringField("Login: ", validators=[DataRequired()])
    name = StringField("Name: ", validators=[DataRequired()])
    surname = StringField("Surname: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[Email()])
    nativeCity = StringField("Native City: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators={DataRequired(), EqualTo('password2', message='Passwords must match')})
    password2 = PasswordField("Password Repeat: ", validators={DataRequired()})
    submit = SubmitField("Submit")

class EditForm(FlaskForm):
    name = StringField("Имя: ", validators=[DataRequired()])
    surname = StringField("Фамилия: ", validators=[DataRequired()])
    nativeCity = StringField("Родной город: ", validators=[DataRequired()])
    submit = SubmitField("Сохранить")

class SetPasswordForm(FlaskForm):
    oldPassword = PasswordField("Old Password", validators={DataRequired()})
    newPassword = PasswordField("New Password: ", validators={DataRequired(), EqualTo('newPassword2')})
    newPassword2 = PasswordField("New Password Repeat: ", validators={DataRequired()})
    submit = SubmitField("Сохранить")

class SetEmailForm(FlaskForm):
    newEmail = StringField("New Email: ", validators=[Email()])
    password = PasswordField("Password", validators={DataRequired()})
    submit = SubmitField("Сохранить")

class DeletePageForm(FlaskForm):
    password = PasswordField("Password", validators={DataRequired()})
    checkBox = BooleanField("Вы уверены?", validators={DataRequired()})
    submit = SubmitField("Подтвердить")

class SetImageForm(FlaskForm):
    image = FileField("Import Image", validators={FileRequired()})
    submit = SubmitField("Сохранить")

class AddImageForm(FlaskForm):
    image = FileField("Import Image", validators={FileRequired()})
    submit = SubmitField("Сохранить")

class AddNewPost(FlaskForm):
    text = StringField("Text: ", validators=[Length(max=1200)])
    image = FileField("Import Image", validators={FileRequired()})
    submit = SubmitField("Сохранить")