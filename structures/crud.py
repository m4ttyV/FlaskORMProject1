from sqlalchemy.orm import joinedload
from structures.extensions import db
from sqlalchemy import func, desc
from structures.serializers import EventSchema, CitySchema, StateSchema, CountrySchema
from structures.models import Event, City, State, Country
from flask import jsonify, abort, make_response, request, Blueprint
from sqlalchemy.orm import aliased

crud_api = Blueprint('crud_api', __name__)
###------------------------------------------------------EXTRAS------------------------------------------------------###
# City-------------------------------------------------------
def get_all_cities():
    return City.query.all()

def insert_city(new_city):
    schema = CitySchema()
    city_obj = schema.load(data=new_city)
    db.session.add(city_obj)
    db.session.commit()
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
    schema = StateSchema()  # Экземпляр схемы
    state_obj = schema.load(data=new_state)
    db.session.add(state_obj)
    db.session.commit()
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
    schema = EventSchema()  # Экземпляр схемы
    country_obj = schema.load(data=new_country)
    db.session.add(country_obj)
    db.session.commit()
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
    schema = EventSchema()  # Экземпляр схемы
    event_obj = schema.load(data=new_event)
    db.session.add(event_obj)
    db.session.commit()
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
    event_update = update_event(id, request.get_json())
    return jsonify({'Event': str(event_update)})

@crud_api.route('/events_post', methods=['POST'])
def create_event():
    event_data = request.get_json()
    new_event = insert_event(event_data)
    return jsonify({'Event': str(new_event)}), 201

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
    event = Event.query.get(event_id)
    if event is None:
        abort(404, description=f"Building with ID {event_id} not found")
    db.session.delete(event)
    db.session.commit()
    return jsonify({"result": True})

# City-------------------------------------------------------

@crud_api.route('/cities/<int:id>', methods=['PUT'])
def update_one_city(id):
    city_update = update_city(id, request.get_json())
    return jsonify({'City': str(city_update)})

@crud_api.route('/cities', methods=['POST'])
def create_city():
    if ('id' in request.json and
            type(request.json['id']) is not int):
        abort(400)
    city_data = request.get_json()
    new_city = insert_city(city_data)
    return jsonify({'City': str(new_city)}), 201

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
    city = City.query.get(city_id)
    if city is None:
        abort(404, description=f"Building with ID {city_id} not found")
    db.session.delete(city)
    db.session.commit()
    return jsonify({"result": True})

# State-------------------------------------------------------

@crud_api.route('/states/<int:id>', methods=['PUT'])
def update_one_state(id):
    state_update = update_state(id, request.get_json())
    return jsonify({'State': str(state_update)})

@crud_api.route('/states', methods=['POST'])
def create_state():
    state_data = request.get_json()
    new_state = insert_state(state_data)
    return jsonify({'State': str(new_state)}), 201

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
    state = State.query.get(state_id)
    if state is None:
        abort(404, description=f"Building with ID {state_id} not found")
    db.session.delete(state)
    db.session.commit()
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
#
# def get_group_stats(group_model, join_condition, group_name_column, table_alias):
#     aliased_model = db.aliased(group_model, name=table_alias)
#
#     query = (
#         db.session.query(
#             getattr(aliased_model, "name").label("group_name"),
#             func.min(Event.duration_seconds).label("min_duration"),
#             func.avg(Event.duration_seconds).label("avg_duration"),
#             func.max(Event.duration_seconds).label("max_duration")
#         )
#         .select_from(Event)
#         .join(City, City.id == Event.city_id)
#         .join(State, State.id == City.state_id)
#         .join(Country, Country.id == State.country_id)
#         .join(aliased_model, join_condition)
#         .group_by(getattr(aliased_model, "name"))
#         .order_by(desc(func.max(Event.duration_seconds)))
#         .limit(30)
#     )
#
#     rows = query.all()
#
#     result = [
#         {
#             "id": i + 1,
#             "Группа": row.group_name,
#             "Минимальная продолжительность": int(row.min_duration),
#             "Средняя продолжительность": int(row.avg_duration),
#             "Максимальная продолжительность": int(row.max_duration)
#         }
#         for i, row in enumerate(rows)
#     ]
#     return result
#
#
# @crud_api.route("/api/top_countries", methods=['GET'])
# def top_countries():
#     return jsonify(get_group_stats(
#         Country,
#         Country.id == State.country_id,
#         Country.name,
#         "country_alias"
#     ))
#
#
# @crud_api.route("/api/top_states", methods=['GET'])
# def top_states():
#     return jsonify(get_group_stats(
#         State,
#         State.id == City.state_id,
#         State.name,
#         "state_alias"
#     ))
#
#
# @crud_api.route("/api/top_cities", methods=['GET'])
# def top_cities():
#     return jsonify(get_group_stats(
#         City,
#         City.id == Event.city_id,
#         City.name,
#         "city_alias"
#     ))

def get_group_stats(group_model, join_condition, table_alias):
    aliased_model = aliased(group_model, name=table_alias)

    try:
        # Build base query
        query = db.session.query(
            getattr(aliased_model, "name").label("group_name"),
            func.min(Event.duration_seconds).label("min_duration"),
            func.avg(Event.duration_seconds).label("avg_duration"),
            func.max(Event.duration_seconds).label("max_duration")
        ).select_from(Event)

        # Joins with aliases to avoid ambiguity
        if group_model == City:
            aliased_city = aliased(City, name="aliased_city")
            aliased_state = aliased(State, name="aliased_state")
            aliased_country = aliased(Country, name="aliased_country")

            query = query.join(aliased_city, aliased_city.id == Event.city_id)
            query = query.join(aliased_state, aliased_state.id == aliased_city.state_id)
            query = query.join(aliased_country, aliased_country.id == aliased_state.country_id)
            query = query.join(aliased_model, aliased_model.id == Event.city_id)

        elif group_model == State:
            aliased_city = aliased(City, name="aliased_city")
            aliased_country = aliased(Country, name="aliased_country")

            query = query.join(aliased_city, aliased_city.id == Event.city_id)
            query = query.join(aliased_model, aliased_model.id == aliased_city.state_id)
            query = query.join(aliased_country, aliased_country.id == aliased_model.country_id)

        else:
            aliased_city = aliased(City, name="aliased_city")
            aliased_state = aliased(State, name="aliased_state")

            query = query.join(aliased_city, aliased_city.id == Event.city_id)
            query = query.join(aliased_state, aliased_state.id == aliased_city.state_id)
            query = query.join(aliased_model, aliased_model.id == aliased_state.country_id)

        # Group and order
        query = query.group_by(getattr(aliased_model, "name"))
        query = query.order_by(desc(func.max(Event.duration_seconds)))
        query = query.limit(30)

        rows = query.all()

        result = [
            {
                "id": i + 1,
                "group": row.group_name,
                "min_duration": int(row.min_duration),
                "avg_duration": int(row.avg_duration),
                "max_duration": int(row.max_duration)
            }
            for i, row in enumerate(rows)
        ]
        return result

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@crud_api.route("/api/top_countries", methods=['GET'])
def top_countries():
    return jsonify(get_group_stats(
        Country,
        Country.id == State.country_id,
        "country_alias"
    ))


@crud_api.route("/api/top_states", methods=['GET'])
def top_states():
    return jsonify(get_group_stats(
        State,
        State.id == City.state_id,
        "state_alias"
    ))


@crud_api.route("/api/top_cities", methods=['GET'])
def top_cities():
    return jsonify(get_group_stats(
        City,
        City.id == Event.city_id,
        "city_alias"
    ))

@crud_api.route("/api/all_rows", methods=['GET'])
def main_table():
    query = (
        db.session.query(
            Event.id.label("event_id"),
            Event.comments.label("comments"),
            Event.date_posted.label("date_posted"),
            Event.duration_seconds.label("duration_seconds"),
            City.name.label("city"),
            State.name.label("state"),
            Country.name.label("country")
        )
        .select_from(Country)
        .join(State)
        .join(City)
        .join(Event)
    )

    # Преобразуем результат в список словарей
    results = [
        {
            "event_id": row.event_id,
            "comments": row.comments,
            "date_posted": row.date_posted if not hasattr(row.date_posted, "isoformat") else row.date_posted.isoformat(),
            "duration_seconds": row.duration_seconds,
            "city": row.city,
            "state": row.state,
            "country": row.country
        }
        for row in query.all()
    ]

    return jsonify(results)
