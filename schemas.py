from pydantic import BaseModel, ConfigDict, Field


class BaseRecipe(BaseModel):
    title: str = Field(
        ..., title="Recipe title.", description="The name of the recipe."
    )
    cooking_time: float = Field(
        ..., title="Cooking time.", description="Cooking time in minutes"
    )


class RecipeFromTop(BaseRecipe):
    views: int = Field(
        ...,
        title="Number of views.",
        description="Number of views. The higher the number of views,"
        " the higher the recipe in the top.",
    )


class RecipeIn(BaseRecipe):
    ingredients: str = Field(
        ..., title="List of ingredients.", description="List of ingredients as a text"
    )
    description: str = Field(
        ...,
        title="Description of the recipe.",
        description="Description of the recipe as a text.",
    )


class RecipeWithDetailedInfo(RecipeIn):
    recipe_id: int = Field(
        ..., title="Primary key", description="Id of recipe in db (primary key)."
    )

    model_config = ConfigDict(from_attributes=True)
