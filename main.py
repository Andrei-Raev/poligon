import os
from json import dump, load
from random import choice
from string import ascii_letters

from flask import Flask, render_template, url_for, request, redirect, make_response
from bred.parser import Parser
from database import session, User

import colorama

colorama.init()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'peritos'

with open('json/logged_users.json', 'r') as f:
    logged_users = load(f)
    if 'None' not in logged_users:
        logged_users.update({"None": {"profile_data": ["../static/avas/gust.webp", "Гость"]}})


def register_user():
    pass


def start_page():
    token = request.cookies.get('user_token')
    if token in logged_users:
        user_data = logged_users[token]['profile_data']
    else:
        user_data = logged_users['None']['profile_data']
    return user_data


def temp_ready():
    temp_path = ''.join(choice(ascii_letters) for _ in range(12))
    while temp_path in os.listdir('static/temp'):
        temp_path = ''.join(choice(ascii_letters) for _ in range(12))
    return temp_path


@app.route('/')
def index():
    user_data = start_page()
    return render_template('main.html', title='Главная страница', user=user_data,
                           person_quest=[{'title': 'Квест в стране отладки', 'value': 67, 'url': 'tq'},
                                         {'title': 'Спонтанное ограбление', 'value': 67, 'url': 'rab'}])


@app.route('/login', methods=['POST', 'GET'])
def login():
    global logged_users
    if request.method == 'POST':
        try:
            username, password = request.form['username'], request.form['password']
            user = session.query(User).filter(User.nickname == username).first()
            if not user:
                return render_template('login.html', message='Произошла ошибка, проверьте данные',
                                       title='Ошибка авторизации', user=start_page())
            if user.hashed_password == password:
                token = ''.join(choice(ascii_letters) for _ in range(12))
                while token in logged_users:
                    token = ''.join(choice(ascii_letters) for _ in range(12))
                logged_users.update({token: {'profile_data': [f'../static/avas/{user.avator}', user.nickname]}})
                res = make_response("<script>window.onload=function(){window.location.replace('../')}</script>")
                res.set_cookie("user_token", token)
                with open('json/logged_users.json', 'w') as f:
                    dump(logged_users, f)
                return res
            else:
                return render_template('login.html', message='Неверный пароль',
                                       title='Ошибка авторизации', user=start_page())
        except Exception:
            pass
    else:

        res = make_response(
            render_template('login.html', message='', title='Авторизация пользователя', user=start_page()))
        return res


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if request.method == 'POST':
        sss = User()
        sss.email = request.form['email']
        sss.name = request.form['name']
        sss.surname = request.form['surname']
        sss.nickname = request.form['nickname']
        sss.avator = 'gust.webp'
        sss.hashed_password = request.form['password']
        session.add(sss)
        session.commit()

        token = ''.join(choice(ascii_letters) for _ in range(12))
        while token in logged_users:
            token = ''.join(choice(ascii_letters) for _ in range(12))
        logged_users.update({token: {'profile_data': [f'../static/avas/{"gust.webp"}', sss.nickname]}})
        res = make_response("<script>window.onload=function(){window.location.replace('../')}</script>")
        res.set_cookie("user_token", token)
        with open('json/logged_users.json', 'w') as f:
            dump(logged_users, f)
        return res
    return render_template('register.html', user=start_page(), title='Регистрация')


@app.route('/quest/<name>')
def load_quest(name):
    need_cookies = False
    user_data = start_page()

    if request.cookies.get('temp_path'):
        parser_to_test = Parser(name, request.cookies.get('temp_path'))
    else:
        temp_path = temp_ready()
        parser_to_test = Parser(name, temp_path)
        need_cookies = True

    try:
        page_content = parser_to_test.get_page(request.args.get('p'))
    except Exception:
        page_content = parser_to_test.get_page('main')

    if not need_cookies:
        return render_template('quest.html', title=parser_to_test.data['title'], user=user_data,
                               quest_text=page_content[0][1], buttons=page_content[1], hedder=page_content[0][0])
    else:

        response = make_response(render_template('quest.html', title=parser_to_test.data['title'], user=user_data,
                                                 quest_text=page_content[0][1], buttons=page_content[1],
                                                 hedder=page_content[0][0]))
        response.set_cookie("temp_path", temp_path)
        return response


@app.route('/account')
def account():
    return redirect('../login')


@app.route('/quit')
def quit_f():
    global logged_users
    res = make_response("<script>window.onload = function () {window.location.replace('../')}</script>")

    try:
        del logged_users[request.cookies.get('user_token')]
    except Exception:
        pass

    res.set_cookie("user_token", "")
    return res


@app.route('/ftp', methods=['GET', 'POST'])
def ftp():
    user_data = [url_for('static', filename='ava.png'), 'Раев Андрей']

    if request.method == "POST":
        files = request.files.getlist('image_file')
        for image in files:
            print('\033[32mSaving:', image.filename, '\033[0m')
            image.save(f'D:/ftp/{image.filename}')
        return render_template('ftp.html', title='FTP', conmplite=True, user=user_data)

    return render_template('ftp.html', title='FTP', conmplite=False, user=user_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

"""    if request.method == "POST":
        files = request.files.getlist('image_file')
        for image in files:
            print('Saving:', image.filename)
            image.save(f'static/{image.filename}')
        return render_template('ftp.html', title='FTP', conmplite=True)

    return render_template('ftp.html', title='FTP', conmplite=False)"""
