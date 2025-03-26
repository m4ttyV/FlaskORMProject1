from config import db
from flask import Blueprint

def main_table():
    query = (
        db.session.query(
            Event.id.label("event_id"),
            Event.comments.label("Comments"),
            Event.date_posted.label("date_posted"),
            Event.duration_seconds.label("duration_seconds"),
            City.name.label("City"),
            State.name.label("State"),
            Country.name.label("Country")
        )
        .select_from(Country)
        .join(State)
        .join(City)
        .join(Event)
    ).limit(100)
    return [query.statement.columns.keys(), query.all()]

#-----------------------------------------------------Buttons-----------------------------------------------------------

def button1():
    """ТОП-10 самых длинных наблюдений НЛО"""
    query = db.session.query(
        Event.date_posted,
        Event.comments,
        Event.duration_seconds,
        City.name.label("city"),
        State.name.label("state"),
        Country.name.label("country")
    ) \
        .select_from(Event).join(City) \
        .join(State) \
        .join(Country) \
        .order_by(db.desc(Event.duration_seconds)) \
        .limit(10)  # ТОП-10 самых длинных наблюдений

    return [query.statement.columns.keys(), query.all()]

def button2():
    """Вывести все события с 2010 года"""
    query = db.session.query(Event.date_posted, Event.comments, Event.duration_seconds, City.name.label("city"),
                             State.name.label("state"), Country.name.label("country")) \
        .select_from(Event).join(City) \
        .join(State) \
        .join(Country) \
        .filter(Event.date_posted >= '2010-01-01').limit(10)  # Фильтр по дате

    return [query.statement.columns.keys(), query.all()]

def button3():
    """Вывести города с наибольшим количеством наблюдений НЛО"""
    query = db.session.query(City.name.label("city"), db.func.count(Event.id).label("sightings"))\
        .join(Event)\
        .group_by(City.name)\
        .order_by(db.desc("sightings"))\
        .limit(10)  # ТОП 10

    return [query.statement.columns.keys(), query.all()]

def button4():
    #Добавить минимальный и максимальный и сделать ещё один аналогичный запрос по другим данным (например город вместо страны)
    """Вывести среднюю продолжительность наблюдений по странам"""
    query = db.session.query(Country.name.label("country"), db.func.avg(Event.duration_seconds).label("avg_duration"))\
        .join(City)\
        .join(State)\
        .join(Country)\
        .group_by(Country.name)\
        .order_by(db.desc("avg_duration"))


    return [query.statement.columns.keys(), query.all()]

def button5():
    """Вывести штаты с наибольшим количеством наблюдений"""
    query = db.session.query(State.name.label("state"), db.func.count(Event.id).label("sightings"))\
        .select_from(Event).join(City)\
        .join(State)\
        .group_by(State.name)\
        .order_by(db.desc("sightings"))\
        .limit(10)  # ТОП 10

    return [query.statement.columns.keys(), query.all()]

def button6():
    """Вывести 1 максимальных наблюдений по странам"""
    query = db.session.query(Country.name.label("country"), Event.duration_seconds.label("max_duration")) \
        .join(City) \
        .join(State) \
        .join(Country) \
        .group_by(Country.name) \
        .order_by(db.desc("max_duration")).limit(2)

    return [query.statement.columns.keys(), query.all()]

def button7():
    """Вывести 1 минимальных наблюдений по странам"""
    query = db.session.query(Country.name.label("country"), Event.duration_seconds.label("min_duration")) \
        .join(City) \
        .join(State) \
        .join(Country) \
        .group_by(Country.name) \
        .order_by(db.asc("min_duration")).limit(1)

    return [query.statement.columns.keys(), query.all()]

#-----------------------------------------------------Classes-----------------------------------------------------------

query = Blueprint('query', __name__)

class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    states = db.relationship('State', cascade="all, delete")
    def __init__(self, name, states):
        self.name = name
        self.states = states

class State(db.Model):
    __tablename__ = 'state'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)

    country = db.relationship('Country', back_populates='states')
    cities = db.relationship('City', cascade="all, delete")
    def __init__(self, name, country_id):
        self.name = name
        self.country_id = country_id

class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)

    state = db.relationship('State', back_populates='cities')
    events = db.relationship('Event', cascade="all, delete")
    def __init__(self, name, state_id):
        self.name = name
        self.state_id = state_id

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.String(100), nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text, nullable=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    city = db.relationship('City', back_populates='events')
    def __init__(self, date_posted, duration_seconds, city_id):
        self.date_posted = date_posted
        self.duration_seconds = duration_seconds
        self.city_id = city_id
# db.app_context().push()
#
# with db.app_context():
#     db.create_all()