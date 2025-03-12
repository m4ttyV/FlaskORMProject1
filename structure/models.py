from app import db
from flask import Blueprint, render_template

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
        .join(City, Event.city_id == City.id) \
        .join(State, City.state_id == State.id) \
        .join(Country, State.country_id == Country.id) \
        .order_by(db.desc(Event.duration_seconds)) \
        .limit(10)  # ТОП-10 самых длинных наблюдений

    return [query.statement.columns.keys(), query.all()]

def button2():
    """Вывести все события с 2010 года"""
    query = db.session.query(Event.date_posted, Event.comments, Event.duration_seconds, City.name.label("city"),
                             State.name.label("state"), Country.name.label("country")) \
        .join(City, Event.city_id == City.id) \
        .join(State, City.state_id == State.id) \
        .join(Country, State.country_id == Country.id) \
        .filter(Event.date_posted >= '2010-01-01')  # Фильтр по дате

    return [query.statement.columns.keys(), query.all()]

def button3():
    """Вывести города с наибольшим количеством наблюдений НЛО"""
    query = db.session.query(City.name.label("city"), db.func.count(Event.id).label("sightings"))\
        .join(Event, Event.city_id == City.id)\
        .group_by(City.name)\
        .order_by(db.desc("sightings"))\
        .limit(10)  # ТОП 10

    return [query.statement.columns.keys(), query.all()]

def button4():
    """Вывести среднюю продолжительность наблюдений по странам"""
    query = db.session.query(Country.name.label("country"), db.func.avg(Event.duration_seconds).label("avg_duration"))\
        .join(City, Event.city_id == City.id)\
        .join(State, City.state_id == State.id)\
        .join(Country, State.country_id == Country.id)\
        .group_by(Country.name)\
        .order_by(db.desc("avg_duration"))

    return [query.statement.columns.keys(), query.all()]

def button5():
    """Вывести штаты с наибольшим количеством наблюдений"""
    query = db.session.query(State.name.label("state"), db.func.count(Event.id).label("sightings"))\
        .join(City, Event.city_id == City.id)\
        .join(State, City.state_id == State.id)\
        .group_by(State.name)\
        .order_by(db.desc("sightings"))\
        .limit(10)  # ТОП 10

    return [query.statement.columns.keys(), query.all()]

query = Blueprint('query', __name__)



class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    states = db.relationship('State', backref='country', cascade='all, delete')

class State(db.Model):
    __tablename__ = 'state'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)

    cities = db.relationship('City', backref='state', cascade='all, delete')

class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)

    events = db.relationship('Event', backref='city', cascade='all, delete')

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.String(100), nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text, nullable=True)

    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

# db.app_context().push()
#
# with db.app_context():
#     db.create_all()