from flask import Flask, render_template, redirect
from flask_login import LoginManager
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user
from data import db_session
from data.login_form import LoginForm
from data.users import User
from data.register import RegisterForm
from sqlalchemy import update
from flask import Flask
from random import randint
from data.inspiration import InspirationForm
import shutil
import requests

K = ''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

def random_color():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    rand_color = (r, g, b)
    return rand_color


'''По дому бродит привиденье.
Весь день шаги над головой.
На чердаке мелькают тени.
По дому бродит домовой.

Везде болтается некстати,
Мешается во все дела,
В халате крадется к кровати,
Срывает скатерть со стола.

Ног у порога не обтерши,
Вбегает в вихре сквозняка
И с занавеской, как с танцоршей,
Взвивается до потолка.

Кто этот баловник-невежа
И этот призрак и двойник?
Да это наш жилец приезжий,
Наш летний дачник-отпускник.

На весь его недолгий роздых
Мы целый дом ему сдаем.
Июль с грозой, июльский воздух
Снял комнаты у нас внаем.

Июль, таскающий в одёже
Пух одуванчиков, лопух,
Июль, домой сквозь окна вхожий,
Всё громко говорящий вслух.

Степной нечесаный растрепа,
Пропахший липой и травой,
Ботвой и запахом укропа,
Июльский воздух луговой.'''


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


@app.route("/idea")
def index():
    return render_template("idea.html", title='Главная')


@app.route("/")
def idea():
    return render_template("index.html", title='Главная')


@app.route("/info")
def info():
    return render_template("info.html", title='Information')


@app.route("/random", methods=['POST', 'GET'])
def random():
    color = random_color()
    r_color = ((255 -color[0]) % 255, (255 -color[1]) % 255, (255 -color[2]) % 255)
    t_color = ((color[0] - 83) % 255, (color[1] - 83) % 255, (color[2] - 83) % 255)
    t1_color = ((color[0] - 83 * 2) % 255, (color[1] - 83 * 2) % 255, (color[2] - 83 * 2) % 255)
    temple = render_template("random.html", title='Random')
    t = temple.replace('$$$', str(color))
    t = t.replace('###', str(r_color))
    t = t.replace('***', str(t_color))
    t = t.replace('!!!', str(t1_color))
    return t


@app.route("/colors", methods=['POST', 'GET'])
def colors():
    return render_template("colors.html", title='Colors')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/inspiration")
def inspiration():
    form = InspirationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        search=form.search.data
        print(search)
        db_sess.add(search)
        db_sess.commit()
        return redirect('/inspitration_nature')
    return render_template("inspiration.html", title='Find inspiration')


@app.route("/inspiration_nature")
def inspitration_nature():
    category = 'nature'
    api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'.format(category)
    for i in range(1, 13):
        name = 'static/img/' + str('img' + str(i)  + '.jpg')
        response = requests.get(api_url, headers={'X-Api-Key': 'T30xzUAIc8Ivt+KJa6eY0g==4UdTnH0kSWCsC0Xy', 'Accept': 'image/jpg'}, stream=True)
        if response.status_code == requests.codes.ok:
            with open(name, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
                out_file.close()
        else:
            print("Error:", response.status_code, response.text)
    return render_template("inspiration_nature.html", title='Nature inspiration')


@app.route("/inspiration_city")
def inspitration_city():
    category = 'city'
    api_url = 'https://api.api-ninjas.com/v1/randomimage?category={}'.format(category)
    for i in range(1, 13):
        name = 'static/img/' + str('img' + str(i)  + '.jpg')
        response = requests.get(api_url, headers={'X-Api-Key': 'T30xzUAIc8Ivt+KJa6eY0g==4UdTnH0kSWCsC0Xy', 'Accept': 'image/jpg'}, stream=True)
        if response.status_code == requests.codes.ok:
            with open(name, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
                out_file.close()
        else:
            print("Error:", response.status_code, response.text)
    return render_template("inspiration_city.html", title='City inspiration')

def main():
    db_session.global_init("db/explorer.sqlite")
    app.run(port=8000)
    print(K)


if __name__ == '__main__':
    main()
