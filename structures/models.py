from structures.extensions import db
from flask import Blueprint

#-----------------------------------------------------Classes-----------------------------------------------------------

query = Blueprint('query', __name__)

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

def maxCountries():
    """Вывести штаты с наибольшим количеством наблюдений"""
    query = db.session.query(State.name.label("state"), db.func.count(Event.id).label("sightings"))\
        .select_from(Event).join(City)\
        .join(State)\
        .group_by(State.name)\
        .order_by(db.desc("sightings")) \
        .limit(30)

    return [query.statement.columns.keys(), query.all()]

def minCountries():
    """Вывести штаты с наибольшим количеством наблюдений"""
    query = db.session.query(State.name.label("state"), db.func.count(Event.id).label("sightings"))\
        .select_from(Event).join(City)\
        .join(State)\
        .group_by(State.name)\
        .order_by("sightings") \
        .limit(30)

    return [query.statement.columns.keys(), query.all()]


def avgCountries():
    #Добавить минимальный и максимальный и сделать ещё один аналогичный запрос по другим данным (например город вместо страны)
    """Вывести среднюю продолжительность наблюдений по странам"""
    query = db.session.query(State.name.label("state"),db.func.avg(Event.duration_seconds).label("avg_duration")) \
        .select_from(Event).join(City) \
        .join(State) \
        .group_by(State.name) \
        .order_by(db.desc("avg_duration")) \
        .limit(30)

    return [query.statement.columns.keys(), query.all()]

class Country(db.Model):
    __tablename__ = 'country'
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    states = db.relationship('State', cascade="all, delete")
    def __init__(self, name, states):
        self.name = name
        self.states = states

class State(db.Model):
    __tablename__ = 'state'
    __table_args__ = {"extend_existing": True}

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
    __table_args__ = {"extend_existing": True}

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
    __table_args__ = {"extend_existing": True}

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