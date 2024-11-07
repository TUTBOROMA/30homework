import datetime
import sys

import pytest
from sqlalchemy import select, func
import factory

sys.path.append('../../hw')

from my_proj.app.models import Client, Parking, ClientParking
from .factories import ClientFactory, ParkingFactory


def test_app_config(app):
    assert app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == "sqlite://"


@pytest.mark.parametrize('route', ['/clients/1', '/clients'])
def test_route_status(web_client, route):
    rv = web_client.get(route)
    assert rv.status_code == 200


def test_create_client(web_client, db):
    client_data = {'name': 'test_name_client_two', 'surname': 'test_surname_client_two',
                   'credit_card': 'creditka', 'car_number': 'х999хх999'}

    resp = web_client.post('/clients', json=client_data)
    assert resp.status_code == 201
    client = db.session.scalar(select(Client).where(Client.id == 2))
    assert client.name == 'test_name_client_two'


def test_create_parking(web_client, db):
    parking_data = {'address': 'test_address_parking_two', 'opened': True,
                    'count_places': 100, 'count_available_places': 100}
    resp = web_client.post('/parkings', json=parking_data)
    assert resp.status_code == 201
    parking = db.session.scalar(select(Parking).where(Parking.id == 2))
    assert parking.address == 'test_address_parking_two'


def test_check_in_parking(web_client, db):
    client = Client(
        name='test_name_client_two',
        surname='test_surname_client_two',
        credit_card='test_credit_card_client_two',
        car_number='test_car_number_two'
    )

    parking = Parking(
        address='test_address_parking_two',
        opened=True,
        count_places=100,
        count_available_places=100
    )

    db.session.add(client)
    db.session.add(parking)
    db.session.commit()

    client_parking_data = {'client_id': 2, 'parking_id': 2}
    resp = web_client.post('/client_parking', json=client_parking_data)
    assert resp.status_code == 201

    client_parking = db.session.scalar(select(ClientParking).where(ClientParking.id == 2))
    assert client_parking.client_id == 2 and client_parking.parking_id == 2
    assert isinstance(client_parking.time_in, datetime.datetime)
    assert client_parking.time_out is None
    assert db.session.get(Parking, 2).count_available_places == 99

    parking.opened = False
    db.session.delete(db.session.get(ClientParking, 2))
    db.session.commit()

    resp = web_client.post('/client_parking', json=client_parking_data)
    assert resp.status_code == 403
    assert b'Parking is occupied.' in resp.data


def test_leaving_parking_lot(web_client, db):
    client_parking_data = {'client_id': 1, 'parking_id': 1}
    resp = web_client.delete('/client_parking', json=client_parking_data)
    assert resp.status_code == 200
    assert db.session.get(Parking, 1).count_available_places == 101

    client = db.session.get(Client, 1)
    client.credit_card = None
    db.session.commit()

    resp = web_client.delete('/client_parking', json=client_parking_data)
    assert b'Credit card is not linked.' in resp.data


def test_create_client_with_factory(web_client, db):
    client: ClientFactory = factory.build(dict, FACTORY_CLASS=ClientFactory)
    resp = web_client.post('/clients', json=client)
    assert resp.status_code == 201
    assert db.session.scalar(select(func.count(Client.id))) == 2


def test_create_parking_with_factory(web_client, db):
    parking: ParkingFactory = factory.build(dict, FACTORY_CLASS=ParkingFactory)
    resp = web_client.post('/parkings', json=parking)
    assert resp.status_code == 201
    assert db.session.scalar(select(func.count(Parking.id))) == 2
