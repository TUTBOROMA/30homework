from pydantic import BaseModel, ConfigDict, conint, constr
from typing_extensions import Annotated

PositiveInt = Annotated[int, conint(gt=0)]
StrictStr50 = Annotated[str, constr(max_length=50)]
StrictStr500 = Annotated[str, constr(max_length=500)]
StrictStr250 = Annotated[str, constr(max_length=250)]


class RecipeBase(BaseModel):
    name: StrictStr50
    cooking_time: PositiveInt
    ingredients: StrictStr500
    description: StrictStr250


class RecipeIn(RecipeBase):
    pass


class RecipeOut(RecipeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class DishBase(BaseModel):
    name: StrictStr50
    views: PositiveInt
    cooking_time: PositiveInt


class DishIn(DishBase):
    pass


class DishOut(DishBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
