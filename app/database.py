from typing import Annotated

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column
from flask_sqlalchemy import SQLAlchemy


int_pk = Annotated[int, mapped_column(primary_key=True)]
str10 = Annotated[str, mapped_column(String(10), nullable=False)]
str50 = Annotated[str, mapped_column(String(50), nullable=False)]
str100 = Annotated[str, mapped_column(String(100), nullable=False)]


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
