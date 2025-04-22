from structures.models import Country, City, State, Event
from structures.extensions import db, ma
from marshmallow import fields

class CitySchema(ma.SQLAlchemyAutoSchema):
    state_name = fields.String(attribute="state.name")
    class Meta:
        model = City
        include_fk = True
        load_instance = True
        sqla_session = db.session
        # fields = ("id", "name", "state_id")
        fields = ("id", "name", "state_name")
class CountrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Country
        include_fk = True
        load_instance = True
        sqla_session = db.session
        fields = ("id", "name")

class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Event
        include_fk = True
        load_instance = True
        sqla_session = db.session
        fields = ("id", "date_posted", "duration_seconds", "comments", "city_id")

class StateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = State
        include_fk = True  # чтобы включать внешние ключи в сериализованный JSON
        load_instance = True  # для десериализации данных обратно в объекты модели
        sqla_session = db.session
        fields = ("id", "name", "country_id")