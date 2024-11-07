import datetime

from flask import current_app, jsonify, request, Blueprint
from sqlalchemy import select


from .database import db
from .models import Client, Parking, ClientParking


bp = Blueprint('index', __name__)


@bp.route('/clients', methods=('GET',))
def get_clients_list():
    clients = db.session.scalars(select(Client)).all()
    return jsonify([client.to_json() for client in clients])


@bp.route('/clients/<int:client_id>', methods=['GET'])
def get_client_by_id(client_id: int):
    client = db.session.scalar(select(Client).where(Client.id == client_id))
    return jsonify(client.to_json())


@bp.route('/clients', methods=('POST',))
def create_client():
    request_data = request.json

    new_client = Client(
        name=request_data['name'],
        surname=request_data['surname'],
        credit_card=request_data['credit_card'],
        car_number=request_data['car_number']
    )

    db.session.add(new_client)
    db.session.commit()

    return '', 201


@bp.route('/parkings', methods=('POST',))
def create_parking():
    request_data = request.json

    new_parking = Parking(
        address=request_data['address'],
        opened=request_data['opened'],
        count_places=request_data['count_places'],
        count_available_places=request_data['count_available_places']
    )

    db.session.add(new_parking)
    db.session.commit()

    return '', 201


@bp.route('/client_parking', methods=('POST',))
def check_in_parking():
    request_data = request.json

    parking = db.session.scalar(select(Parking).where(Parking.id == request_data['parking_id']))

    if parking.opened and parking.count_available_places > 0:
        new_client_parking = ClientParking(
            client_id=request_data['client_id'],
            parking_id=request_data['parking_id'],
            time_in=datetime.datetime.now()
        )

        db.session.add(new_client_parking)
        parking.count_available_places -= 1

        db.session.commit()

        return '', 201

    return 'Parking is occupied.', 403


@bp.route('/client_parking', methods=('DELETE',))
def leaving_parking_lot():
    request_data = request.json
    client = db.session.scalar(select(Client).where(Client.id == request_data['client_id']))

    if client.credit_card:
        parking = db.session.scalar(select(Parking).where(Parking.id == request_data['parking_id']))

        client_parking = db.session.scalar(select(ClientParking)
                                           .where(ClientParking.client_id == request_data['client_id'],
                                                  ClientParking.parking_id == request_data['parking_id']))

        if client_parking:
            client_parking.time_out = datetime.datetime.now()
            parking.count_available_places += 1

        db.session.commit()

        return '', 200

    else:
        return 'Credit card is not linked.', 403
