import sqlite3
from flask import g
from main import *


def connect_db():
  """Соединяет с указанной базой данных."""
  rv = sqlite3.connect(app.config['DATABASE'])
  rv.row_factory = sqlite3.Row
  return rv


def init_db():
  """Инициализация базы данных в первый раз"""
  with app.app_context():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
      db.cursor().executescript(f.read())
    db.commit()


def get_db():
  """Если ещё нет соединения с базой данных, открыть новое - для
  текущего контекста приложения
  """
  if not hasattr(g, 'sqlite_db'):
    g.sqlite_db = connect_db()
  return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
  """Заканчивает соединение с базой данных"""
  if hasattr(g, 'sqlite_db'):
    g.sqlite_db.close()


#Вставка новой строки в таблицы
def insert_into_table(table, *args):
  db = get_db()
  argum = ", ".join([str(arg) for arg in args])
  requests = [request.form[arg] for arg in args]
  question = ", ".join(['?' for arg in args])
  db.execute(
      'insert into ' + str(table) + ' (' + argum + ')' + 'values ' + '(' +
      question + ');', requests)
  db.commit()


#Доставка из базы данных строк из таблицы
def select_from_table(table, column_sort, order, *args):
  db = get_db()
  argum = ", ".join([str(arg) for arg in args])
  cur = db.execute('select ' + argum + ' from ' + table + ' order by ' + column_sort + ' ' + order + ';')
  result = cur.fetchall()
  db.commit()
  return result


#создание таблиц
def create_table(table_name, arg):
  db = get_db()
  db.execute("create table " + table_name + " (" + arg + ");")
  db.commit()