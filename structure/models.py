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
    query = (
        db.session.query(
            Event.id.label("1"),
            Event.comments.label("1"),
            Event.date_posted.label("1"),
            Event.duration_seconds.label("1"),
            City.name.label("1"),
            State.name.label("1"),
            Country.name.label("1")
        )
        .select_from(Country)
        .join(State)
        .join(City)
        .join(Event)
    ).limit(100)
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