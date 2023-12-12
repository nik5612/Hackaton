#Базовые импорты
import os
import time
#Импорты сторонних библиотек
from flask import Flask, request, session, redirect, url_for, render_template
from flask_socketio import SocketIO
from waitress import serve
from gevent.pywsgi import WSGIServer
#Импорты файлов проекта
from gen_docx import *
from sql_inject import *
from user_ import *

app = Flask(__name__)
app.config.from_object(__name__)

socketio = SocketIO(app, cors_allowed_origins="*")





##############socketio##############################
@socketio.on('connect')
def handle_connect():
  print('User connected')


@socketio.on('disconnect')
def handle_disconnect():
  print('User disconnected')


@socketio.on('user_join')
def handle_user_join(username):
  print('{username} joins chat')


@socketio.on('new_message')
def handle_new_message(message):
  print(' {message}')
  emit('chat', {'message': message}, broadcast=True)
########################################################

app.config.update(
    dict(DATABASE=os.path.join(app.root_path, 'flask.db'),
         DEBUG=True,
         LOGIN_IN = False,
         SECRET_KEY='development_key'))
app.config.from_envvar('FLASK_SETTINGS', silent=True)
#session['logged_in'] = False

@app.route('/')
def index():
  return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
  if request.method == 'POST':
    action = request.form['action']
    if action == 'docx_button':
      sec_utc = time.time()
      time_utc = time.gmtime(sec_utc)
      #time.strftime('%d.%m.%Y', time_utc)
      gen_docx(str(time.strftime('Договор %d.%m.%Y %H.%M.%S', time_utc)),
               text_dict)
      return redirect(url_for('dashboard'))
  title = "Дашборд"
  return render_template('dashboard.html', students=timeless(), title=title)


@app.route('/spisok')
def spisok():
  return render_template('spisok.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
  if request.method == 'POST':
    action = request.form['action']
    if action == 'docx_button':
      sec_utc = time.time()
      time_utc = time.gmtime(sec_utc)
      #time.strftime('%d.%m.%Y', time_utc)
      gen_docx(str(time.strftime('Договор %d.%m.%Y %H.%M.%S', time_utc)),
               text_dict)
      return redirect(url_for('chat'))
  return render_template('chat.html')


######################################################################################
@app.route('/test_jinja')
def test_jinja():

  title = "Тестовая страница дивы"
  return render_template('test jinja.html', students=timeless(), title=title)


#######################################################################################


@app.route('/singup', methods=['GET', 'POST'])
def singup():
  if request.method == 'POST':
    insert_into_table("main_table", "company", "email", "password", "rule",
                      "first_name", "last_name", "patronymic", "tel_number")
    return redirect(url_for('login'))
  return render_template('singup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  #if session['logged_in'] == True:
    #return redirect(url_for('dashboard'))
  rows_db = []
  all_email = []
  all_password = []
  error = None
  if request.method == 'POST':
    log_and_pass = select_from_table("main_table", "email", "asc", "email",
                                     "password")
    rows_db = [dict(row) for row in log_and_pass]
    for i in rows_db:
      all_email.append(i["email"])
    for i in rows_db:
      all_password.append(i["password"])
    if request.form['email'] not in all_email:
      error = 'Неверный адрес электронной почты'
    elif request.form['password'] not in all_password:
      error = 'Неверный пароль'
    else:
      session['logged_in'] = True
      return redirect(url_for('dashboard'))
  return render_template('login.html', error=error)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81, debug=False)# - это запуск сервера разработки
#########################################################################################
  #serve(app, host="0.0.0.0", port=8080)# - этой командой запускать уже в продакшене
#########################################################################################
  #http_server = WSGIServer(('', 81), app)# - Это второй вариант запуска
  #http_server.serve_forever()# - приложения в продакшене