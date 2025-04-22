from sqlalchemy.orm import joinedload

from structures.extensions import db
from sqlalchemy import func
from structures.serializers import EventSchema, CitySchema, StateSchema, CountrySchema
from structures.models import Event, City, State, Country
from flask import jsonify, abort, make_response, request, Blueprint
from marshmallow import ValidationError

crud_api = Blueprint('crud_api', __name__)
# curl -i -H "Content-Type:application/json" -X PUT -d "{\"height\":500}" http://localhost:5000/buildings/65
# curl -i -H "Content-Type:application/json" --data "{\"title\":\"Пекинская Башня CITIC\", \"city_id\":\"23\", \"year\":\"2018\"}" http://localhost:5000/buildings
###------------------------------------------------------EXTRAS------------------------------------------------------###
# City-------------------------------------------------------
def get_all_cities():
    return City.query.all()

def insert_city(new_city):
    # item = CitySchema.load(new_city, session=db.session)
    schema = CitySchema()
    city_obj = schema.load(data=new_city)
    db.session.add(city_obj)
    db.session.commit()
    # возвращаем вставленную запись, то есть запись с максимальным id
    return City.query. \
        filter(City.id == db.session.query(func.max(City.id))). \
        one_or_none()

def update_city(city_id, update_par):
    City.query.filter(City.id == city_id).update(update_par)
    db.session.commit()
    return get_city(city_id)

# State-------------------------------------------------------
def get_all_states():
    return State.query.all()

def insert_state(new_state):
    # item = StateSchema.load(new_state, session=db.session)
    schema = StateSchema()  # Экземпляр схемы
    state_obj = schema.load(data=new_state)
    db.session.add(state_obj)
    db.session.commit()
    # возвращаем вставленную запись, то есть запись с максимальным id
    return State.query. \
        filter(State.id == db.session.query(func.max(State.id))). \
        one_or_none()

def update_state(state_id, update_par):
    State.query.filter(State.id == state_id).update(update_par)
    db.session.commit()
    return get_state(state_id)

# Country-------------------------------------------------------
def get_all_countries():
    return Country.query.all()

def insert_country(new_country):
    # item = CountrySchema.load(new_event, session=db.session)
    schema = EventSchema()  # Экземпляр схемы
    country_obj = schema.load(data=new_country)
    db.session.add(country_obj)
    db.session.commit()
    # возвращаем вставленную запись, то есть запись с максимальным id
    return Country.query. \
        filter(Country.id == db.session.query(func.max(Country.id))). \
        one_or_none()

def update_country(country_id, update_par):
    Country.query.filter(Country.id == country_id).update(update_par)
    db.session.commit()
    return get_country(country_id)

# Event-------------------------------------------------------

def get_all_events():
    return Event.query.all()

def insert_event(new_event):
    # item = EventSchema.load(new_event, session=db.session)
    schema = EventSchema()  # Экземпляр схемы
    event_obj = schema.load(data=new_event)
    db.session.add(event_obj)
    db.session.commit()
    # возвращаем вставленную запись, то есть запись с максимальным id
    return Event.query. \
        filter(Event.id == db.session.query(func.max(Event.id))). \
        one_or_none()

def update_event(event_id, update_par):
    Event.query.filter(Event.id == event_id).update(update_par)
    db.session.commit()
    return get_event(event_id)

###------------------------------------------------------ERRORS------------------------------------------------------###
@crud_api.errorhandler(400)
def bad_request_error(error):
    response = {
        "error": "Bad Request",
        "message": str(error)
    }
    return jsonify(response), 400

@crud_api.errorhandler(404)
def not_found(error):
 return make_response(jsonify({'error': 'Not found'}), 404)

###--------------------------------------------------------API-------------------------------------------------------###

# Events-------------------------------------------------------
@crud_api.route('/event_put/<int:id>', methods=['PUT'])
def update_one_event(id):
    # получить информацию о здании с указанным id
    event = get_event(id)
    if event is None or not request.json:
        abort(404)
    if ('id' in request.json and
            type(request.json['id']) is not int):
        abort(400)
    event_update = update_event(id, request.get_json())
    return jsonify({'Event': str(event_update)})

@crud_api.route('/events_post', methods=['POST'])
def create_event():
    if ('id' in request.json and
            type(request.json['id']) is not int):
        abort(400)
    new_event = request.get_json()
    event_new = insert_event(new_event)
    return jsonify({'Event': str(event_new)}), 201

@crud_api.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    event_schema = EventSchema()
    event = Event.query.filter(Event.id == id).first()
    if event is None:
        abort(404)
    return jsonify({"Event": event_schema.dump(event)})

@crud_api.route('/events', methods=['GET'])
def get_events():
    event_schema = EventSchema(many=True)
    build = get_all_events()
    return jsonify({"Event": event_schema.dump(build)})

@crud_api.route('/event_del/<int:event_id>', methods=['DELETE'])
def delete_one_event(event_id):
    # Поиск записи по ID
    event = Event.query.get(event_id)
    # Если запись не найдена, возвращаем ошибку 404
    if event is None:
        abort(404, description=f"Building with ID {event_id} not found")
    # Удаляем запись
    db.session.delete(event)
    db.session.commit()
    # Возвращаем успешный результат
    return jsonify({"result": True})

# City-------------------------------------------------------

@crud_api.route('/cities/<int:id>', methods=['PUT'])
def update_one_city(id):
    # получить информацию о здании с указанным id
    city = get_city(id)
    if city is None or not request.json:
        abort(404)
    if ('id' in request.json and
            type(request.json['id']) is not int):
        abort(400)
    city_update = update_city(id, request.get_json())
    return jsonify({'City': str(city_update)})

@crud_api.route('/cities', methods=['POST'])

def create_city():
    if ('id' in request.json and
            type(request.json['id']) is not int):
        abort(400)
    new_city = request.get_json()
    city_new = insert_city(new_city)
    return jsonify({'City': str(city_new)}), 201

@crud_api.route('/cities/<int:id>', methods=['GET'])
def get_city(id):
    city_schema = CitySchema()
    city = City.query.options(joinedload(City.state)).filter(City.id == id).first()
    if city is None:
        abort(404)

    return jsonify({"City": city_schema.dump(city)})

@crud_api.route('/cities', methods=['GET'])
def get_cities():
    city_schema = CitySchema(many=True)
    city = get_all_cities()
    return jsonify({"City": city_schema.dump(city)})

@crud_api.route('/cities/<int:city_id>', methods=['DELETE'])
def delete_one_city(city_id):
    # Поиск записи по ID
    city = City.query.get(city_id)
    # Если запись не найдена, возвращаем ошибку 404
    if city is None:
        abort(404, description=f"Building with ID {city_id} not found")
    # Удаляем запись
    db.session.delete(city)
    db.session.commit()
    # Возвращаем успешный результат
    return jsonify({"result": True})

# State-------------------------------------------------------

@crud_api.route('/states/<int:id>', methods=['PUT'])
def update_one_state(id):
    # получить информацию о здании с указанным id
    state = get_state(id)
    if state is None or not request.json:
        abort(404)
    if ('id' in request.json and
            type(request.json['id']) is not int):
        abort(400)
    state_update = update_state(id, request.get_json())
    return jsonify({'State': str(state_update)})

@crud_api.route('/states', methods=['POST'])
def create_state():
    if ('id' in request.json and
            type(request.json['id']) is not int):
        abort(400)
    new_state = request.get_json()
    state_new = insert_state(new_state)
    return jsonify({'State': str(state_new)}), 201

@crud_api.route('/states/<int:id>', methods=['GET'])
def get_state(id):
    state_schema = StateSchema()
    state = State.query.filter(State.id == id).first()
    if state is None:
        abort(404)
    return jsonify({"State": state_schema.dump(state)})


@crud_api.route('/states', methods=['GET'])
def get_states():
    state_schema = StateSchema(many=True)
    state = get_all_states()
    return jsonify({"State": state_schema.dump(state)})

@crud_api.route('/states/<int:state_id>', methods=['DELETE'])
def delete_one_state(state_id):
    # Поиск записи по ID
    state = State.query.get(state_id)
    # Если запись не найдена, возвращаем ошибку 404
    if state is None:
        abort(404, description=f"Building with ID {state_id} not found")
    # Удаляем запись
    db.session.delete(state)
    db.session.commit()
    # Возвращаем успешный результат
    return jsonify({"result": True})

# Country-------------------------------------------------------

@crud_api.route('/country_put/<int:id>', methods=['PUT'])
def update_one_country(id):
    # получить информацию о здании с указанным id
    country = get_country(id)
    if country is None or not request.json:
        abort(404)
    if ('id' in request.json and
            type(request.json['id']) is not int):
        abort(400)
    country_update = update_country(id, request.get_json())
    return jsonify({'Country': str(country_update)})

@crud_api.route('/countries_post', methods=['POST'])
def create_country():
    if ('id' in request.json and
            type(request.json['id']) is not int):
        abort(400)
    new_country = request.get_json()
    country_new = insert_state(new_country)
    return jsonify({'Country': str(country_new)}), 201

@crud_api.route('/countries/<int:id>', methods=['GET'])
def get_country(id):
    country_schema = CountrySchema()
    country = Country.query.filter(Country.id == id).first()
    if country is None:
        abort(404)
    return jsonify({"Country": country_schema.dump(country)})

@crud_api.route('/countries', methods=['GET'])
def get_countries():
    country_schema = CountrySchema(many=True)
    country = get_all_countries()
    return jsonify({"Country": country_schema.dump(country)})

@crud_api.route('/country_del/<int:country_id>', methods=['DELETE'])
def delete_one_country(country_id):
    # Поиск записи по ID
    country = Country.query.get(country_id)
    # Если запись не найдена, возвращаем ошибку 404
    if country is None:
        abort(404, description=f"Building with ID {country_id} not found")
    # Удаляем запись
    db.session.delete(country)
    db.session.commit()
    # Возвращаем успешный результат
    return jsonify({"result": True})
# End-------------------------------------------------------
