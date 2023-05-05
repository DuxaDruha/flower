from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class InspirationForm(FlaskForm):
    search = StringField('Your search', validators=[DataRequired()])
    submit = SubmitField('Submit')