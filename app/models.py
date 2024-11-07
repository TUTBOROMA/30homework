from typing import Optional
from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .database import db, str10, str50, str100, int_pk


class Client(db.Model):
    """
    Модель Client

    Attributes:
        id (int)
        name (str)
        surname (str)
        credit_card (str)
        car_number (str)
    """

    __tablename__ = 'client'

    id: Mapped[int_pk]
    name: Mapped[str50]
    surname: Mapped[str50]
    credit_card: Mapped[Optional[str50]] = mapped_column(nullable=True)
    car_number: Mapped[Optional[str10]] = mapped_column(nullable=True)

    def __repr__(self):
        return f'Клиент {self.name} {self.surname}'

    def to_json(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Parking(db.Model):
    """
    Модель Parking

    Attributes:
        id (int)
        address (str)
        opened (bool)
        count_places (int)
        count_available_places (str)
    """

    __tablename__ = 'parking'

    id: Mapped[int_pk]
    address: Mapped[str100]
    opened: Mapped[Optional[bool]] = mapped_column(nullable=True)
    count_places: Mapped[int]
    count_available_places: Mapped[int]

    def __repr__(self):
        return f'Парковка {self.address}'

    def to_json(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class ClientParking(db.Model):
    """
    Модель ClientParking

    Attributes:
        id (int)
        client_id (int)
        parking_id (int)
        time_in (datetime)
        time_out (datetime)
    """

    __tablename__ = 'client_parking'
    __table_args__ = (
        UniqueConstraint('client_id', 'parking_id'),
    )

    id: Mapped[int_pk]
    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'))
    parking_id: Mapped[int] = mapped_column(ForeignKey('parking.id'))
    time_in: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    time_out: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def __repr__(self):
        return f'Клиент {self.client_id} место {self.parking_id}'

    def to_json(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
