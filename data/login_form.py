from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

'''
    Ночевала
    тучка
    золотая
    На
    груди
    утеса - великана;
    Утром
    в
    путь
    она
    умчалась
    рано,
    По
    лазури
    весело
    играя;

    Но
    остался
    влажный
    след
    в
    морщине
    Старого
    утеса.Одиноко
    Он
    стоит, задумался
    глубоко,
    И
    тихонько
    плачет
    он
    в
    пустыне. '''
