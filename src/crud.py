from sqlalchemy import desc, select, update

from .database import session
from .models import Dish, Recipe


async def add_db(obj: Recipe | Dish) -> None:
    session.add(obj)
    await session.commit()
    await session.refresh(obj)


async def all_recipe_db():
    result = await session.execute(
        select(Dish).order_by(desc(Dish.views), Dish.cooking_time)
    )
    return result.scalars().all()


async def get_recipe_db(recipe_id: int) -> Recipe | None:
    return await session.get(Recipe, recipe_id)


async def counting_recipe_views_db(recipe_id: int) -> None:
    await session.execute(
        update(Dish).where(Dish.id == recipe_id).values(views=Dish.views + 1)
    )
    await session.commit()


async def delete_recipe_by_id_test(recipe_id: int):
    for o in [Recipe, Dish]:
        obj = await session.get(o, recipe_id)
        await session.delete(obj)
        await session.commit()
