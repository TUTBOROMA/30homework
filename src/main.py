from contextlib import asynccontextmanager
from typing import AsyncGenerator, List

from fastapi import FastAPI, HTTPException, status

from .crud import add_db, all_recipe_db, counting_recipe_views_db, get_recipe_db
from .database import engine, session
from .log_config_dict import log_config
from .models import Base, Dish, Recipe
from .schemas import DishOut, RecipeBase, RecipeOut


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await session.close()
    await engine.dispose()


app: FastAPI = FastAPI(lifespan=lifespan)


@app.get(
    "/recipes",
    response_model=List[DishOut],
    status_code=status.HTTP_200_OK,
    tags=["recipes"],
    summary="Get all recipes",
)
async def get_recipes() -> List[Dish]:
    return await all_recipe_db()


@app.get(
    "/recipes/{recipe_id}",
    response_model=RecipeOut,
    status_code=status.HTTP_200_OK,
    tags=["recipes id"],
    summary="Get a recipe by ID",
)
async def get_recipes_by_id(recipe_id: int) -> Recipe:
    result: Recipe | None = await get_recipe_db(recipe_id)
    if result is not None:
        await counting_recipe_views_db(recipe_id)
        return result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Recipe by {recipe_id} not found!",
    )


@app.post(
    "/recipes",
    response_model=RecipeOut,
    status_code=status.HTTP_201_CREATED,
    tags=["all recipes"],
    summary="Add new recipe",
)
async def prescription_information(recipes: RecipeBase) -> Recipe:
    new_recipe: Recipe = Recipe(**recipes.model_dump())
    new_dish: Dish = Dish(name=recipes.name, cooking_time=recipes.cooking_time)
    await add_db(new_recipe)
    await add_db(new_dish)
    return new_recipe


if __name__ == "__main__":
    from pathlib import Path

    import uvicorn

    app_dir = Path(__file__).parent.as_posix()
    uvicorn.run("main:app", reload=True, app_dir=app_dir, log_config=log_config)
