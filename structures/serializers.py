from structures.models import Country, City, State, Event
from structures.extensions import db, ma
from marshmallow import fields

class CountrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Country
        load_instance = True
        sqla_session = db.session
        #fields = ("id", "name")
        fields = ("id", "name", "country_name")

class StateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = State
        load_instance = True  # для десериализации данных обратно в объекты модели
        sqla_session = db.session
        fields = ("id", "name", "country_id")

    country_name = ma.Nested(CountrySchema())
    country_id = ma.auto_field()

class CitySchema(ma.SQLAlchemyAutoSchema):
    # state_name = fields.String(attribute="state.name")
    class Meta:
        model = City
        load_instance = True
        sqla_session = db.session
        fields = ("id", "name", "state_id")
        #fields = ("id", "name", "state_name")
    state_name = ma.Nested(StateSchema())
    state_id = ma.auto_field()

class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Event
        load_instance = True
        sqla_session = db.session
        fields = ("id", "date_posted", "duration_seconds", "comments", "city_id")

    city_name = ma.Nested(CitySchema())
    city_id = ma.auto_field()