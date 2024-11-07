from sqlalchemy import Column, Float, Integer, String, Text

from database import Base


class Recipe(Base):
    __tablename__: str = "recipe"

    recipe_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    views = Column(Integer, default=0, nullable=False)
    cooking_time = Column(Float, nullable=False)
    ingredients = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
