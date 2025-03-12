import csv
from sqlalchemy import func, desc
from app import app, db
from structure.models import Country, City, State, Event


def get_or_create(session, model, defaults=None, **kwargs):
    """Получает существующую запись или создаёт новую"""
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        params = {**kwargs, **(defaults or {})}
        instance = model(**params)
        session.add(instance)
        session.flush()  # flush сохраняет объект без коммита всей транзакции
        return instance


def load_data(file_path):
    with app.app_context():
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            next(reader)  # Пропускаем заголовок
            for item in reader:
                country_name = item['country'].strip() if item['country'] else 'Unknown'
                state_name = item['state'].strip() if item['state'] else 'Unknown'
                city_name = item['city'].strip() if item['city'] else 'Unknown'

                # Получаем или создаем страну
                country = get_or_create(db.session, Country, name=country_name)

                # ✅ Исправлено: ищем штат по `name` и `country_id`
                state = get_or_create(db.session, State, name=state_name, country_id=country.id)

                # ✅ Исправлено: проверяем `name` + `state_id`, чтобы избежать дубликатов городов
                city = get_or_create(db.session, City, name=city_name, state_id=state.id)

                # Обрабатываем duration_seconds
                try:
                    duration_clean = item['duration (seconds)'].replace('`', '').replace(',', '.').strip()
                    duration_value = int(round(float(duration_clean)))
                except (ValueError, TypeError):
                    duration_value = None  # Если не удалось преобразовать, записываем None

                # Создаем событие только если город успешно найден
                if city:
                    event = Event(
                        date_posted=item['date posted'].strip(),
                        duration_seconds=duration_value,
                        comments=item['comments'].strip(),
                        city_id=city.id
                    )
                    db.session.add(event)

            db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        load_data('./data/ufo_sightings_scrubbed.csv')
