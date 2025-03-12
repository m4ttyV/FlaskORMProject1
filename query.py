from flask import Blueprint, render_template
from app import db
from structure.models import Event, City, State, Country
#
# query = Blueprint('query', __name__)
#
#
#
# @query.route('/query1')
# def query1():
#     # Пример запроса: города с наибольшим количеством наблюдений
#     result = db.session.query(City.name, db.func.count(Event.id)).join(Event).group_by(City.name).all()
#     return render_template('index.html', data=result)
#
# @query.route('/query2')
# def query2():
#     # Пример запроса: средняя продолжительность наблюдений по странам
#     result = db.session.query(Country.name, db.func.avg(Event.duration_seconds)).\
#         join(State).join(City).join(Event).group_by(Country.name).all()
#     return render_template('index.html', data=result)
#
# @query.route('/query3')
# def query3():
#     # Пример запроса: штаты с самым коротким временем наблюдения
#     result = db.session.query(State.name, db.func.min(Event.duration_seconds)).\
#         join(City).join(Event).group_by(State.name).all()
#     return render_template('index.html', data=result)
#
# @query.route('/query4')
# def query4():
#     # Пример запроса: Топ-5 самых популярных штатов
#     result = db.session.query(State.name, db.func.max(State.name)).group_by(State.name).all()
#     return render_template('index.html', data=result)
#
# @query.route('/query5')
# def query5():
#     # Пример запроса: Среднее время наблюдения по городам
#     result = db.session.query(City.name, db.func.avg(Event.duration_seconds)).\
#         join(Event).group_by(City.name).all()
#     return render_template('index.html', data=result)
