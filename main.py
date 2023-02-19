from flask import Flask, make_response, jsonify, request, render_template, redirect
import datetime
import re
from pprint import pprint

import pydantic
from flask import jsonify, abort, request, Blueprint, render_template, redirect
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from data import db_session
from forms.registration import RegisterForm
from data import db_session
from data.couriers import Courier
from data.users import User
from forms.login import LoginForm
from forms.homa_page import HomeForm
from forms.user_edit import EditAboutForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
x = 0
login_manager = LoginManager()
login_manager.init_app(app)
courier_fields = {'courier_id', 'courier_type', 'regions', 'working_hours'}
order_fields = {'order_id', 'weight', 'region', 'delivery_hours'}
c_type = {'foot': 10, 'bike': 15, 'car': 50}
rev_c_type = {10: 'foot', 15: 'bike', 50: 'car'}
kd = {10: 2, 15: 5, 50: 9}
CODE = 'zhern0206eskiy'
PATTERN = r = re.compile('.{2}:.{2}-.{2}:.{2}')


@app.errorhandler(401)
def page_not_found(e):
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/', methods=['GET', 'POST'])
def start():
    form = HomeForm()

    url = "https://img.freepik.com/premium-photo/nice-positive-smart-people-sitting-together-and-discussing-their-project-while-working-in-team_376548-285.jpg?w=1380"
    url2 = "https://img.freepik.com/premium-vector/business-persons-planning-meeting-schedule-using-huge-calendar_74855-19691.jpg"
    return render_template('homepage.html', url=url, url2=url2, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data,
            subject=form.subject.data,
            grade=form.grade.data,
            user_type=int(form.is_courier.data)
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/admins', methods=['GET', "POST"])
@login_required
def make_admins():
    if current_user.user_type < 3:
        return redirect('/')
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return render_template('existing_users.html', title='Существующие пользователи',
                           items=users)


@app.route('/admins/<user_id>', methods=['GET', "POST"])
@login_required
def make_admin(user_id):
    if current_user.user_type < 3:
        return redirect('/')
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if db_sess.query(User).get(user.c_id):
        courier_id = user.c_id
        courier = db_sess.query(Courier).filter(Courier.id == courier_id).first()
        # return jsonify({'message': 'no courier with this id'}), 400
        user = db_sess.query(User).filter(User.c_id == courier_id).first()
        user.c_id = None
        db_sess.delete(courier)
    user.user_type = 3
    db_sess.commit()
    return render_template('result.html', u=str({"Status": 'Ok, now user is admin'}))


@app.route('/timetable', methods=['GET'])
def show_timetable():
    return render_template('timetable.html')


@app.route('/lk', methods=['GET'])
def show_lk():
    return render_template('lk.html')


@app.route('/teachers', methods=['GET'])
def show_teachers():
    urls = [
        "https://i.pinimg.com/564x/7b/32/ac/7b32ac3bc074a2e80486df5ac11a4092.jpg",
        "https://i.pinimg.com/564x/29/23/16/292316c5a7e0bbbb96bdff5c95448e81.jpg",
        "https://i.pinimg.com/564x/88/14/0b/88140b5d064fd41d4f95697070b176d0.jpg"
    ]
    return render_template('teachers.html', url1=urls[0], url2=urls[1], url3=urls[2])


@app.route('/users/edit', methods=['POST', 'GET'])
@login_required
def change_about():
    if current_user.user_type > 1:
        return redirect('/')
    form = EditAboutForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        user.about = form.about.data
        db_sess.commit()
        # print(form.about.data)
        return redirect('/')
    form.about.data = current_user.about
    return render_template('edit_user.html', form=form, title="Изменить резюме")


@app.route('/users/get', methods=['POST', 'GET'])
@login_required
def inside_about():
    if current_user.user_type > 1:
        return redirect('/')
    return render_template('user_info.html', title="О пользователе", about=current_user.about)


@app.route('/clear', methods=['POST', 'GET'])
@login_required
def clear():
    # if request.json['code'] != CODE:
    #     return jsonify({"error": "wrong code"}), 400
    logout_user()
    db_sess = db_session.create_session()
    db_sess.query(Courier).delete()
    db_sess.query(User).delete()
    db_sess.commit()
    user = User(
        name='admin',
        email='admin@admin.com',
        about='main admin',
        user_type=3
    )
    user.set_password('admin')
    db_sess.add(user)
    db_sess.commit()
    return redirect('/')
    # return jsonify({'status': 'all data cleared'}), 201


def main():
    db_session.global_init("db/students.db")
    app.run()
    # app.run(port=8080)
    # serve(app, host='127.0.0.1', port=8080)
    # app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
