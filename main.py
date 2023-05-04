from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user
from data import db_session
from data.login_form import LoginForm
from data.users import User
from data.register import RegisterForm
from sqlalchemy import update

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="К сожалению, такя почта уже используется другим пользователем")
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            adress=form.adress.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/")
def index():
    return render_template("index.html", title='Главная')


@app.route("/info")
def info():
    return render_template("info.html", title='Information')






@app.route("/random", methods=['POST', 'GET'])
def random():
    COLOR = '8b00ff'
    form = LoginForm()
    if form.validate_on_submit():
        COLOR = request.form['color']
        db_session.execute(update(users).where(users.id == current_user.id).values(color=COLOR))
        print(COLOR)
    return render_template("random.html", title='Random')






@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/mars_explorer.sqlite")
    app.run(port=8000, debug=True)


if __name__ == '__main__':
    main()
