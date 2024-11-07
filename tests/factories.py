import random

import factory

from my_proj.app.models import Client, Parking
from my_proj.app.database import db


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    car_number = factory.Faker('license_plate')
    credit_card = factory.Faker('credit_card_number') if random.randint(0, 1) == 1 else None


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker('address')
    opened = factory.Faker('pybool')
    count_places = factory.Faker('random_int', min=10, max=200)
    count_available_places = factory.lazy_attribute(lambda a: random.randint(0, a.count_places + 1))
