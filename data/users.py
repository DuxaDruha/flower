import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from werkzeug.security import generate_password_hash, check_password_hash
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    adress = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    #books = orm.relationship("Books", back_populates='user')


    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


'''Чисто вечернее небо,
Ясны далекие звезды,
Ясны как счастье ребенка;
О! для чего мне нельзя и подумать:
Звезды, вы ясны, как счастье мое!

Чем ты несчастлив,
Скажут мне люди?
Тем я несчастлив,
Добрые люди, что звезды и небо
Звезды и небо! — а я человек!..

Люди друг к другу
Зависть питают;
Я же, напротив,
Только завидую звездам прекрасным,
Только их место занять бы желал.'''