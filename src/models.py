from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Dish(Base):
    name: Mapped[str]
    views: Mapped[int] = mapped_column(default=0)
    cooking_time: Mapped[int]


class Recipe(Base):
    name: Mapped[str]
    cooking_time: Mapped[int]
    ingredients: Mapped[str]
    description: Mapped[str]
