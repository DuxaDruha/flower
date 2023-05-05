from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    adress = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


'''
Листья в поле пожелтели,
И кружатся и летят;
Лишь в бору поникши ели
Зелень мрачную хранят.

Под нависшею скалою,
Уж не любит, меж цветов,
Пахарь отдыхать порою
От полуденных трудов.

Зверь, отважный, поневоле
Скрыться где-нибудь спешит.
Ночью месяц тускл, и поле
Сквозь туман лишь серебрит.
'''
