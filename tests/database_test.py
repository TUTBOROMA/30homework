from typing import List, Dict, Final

from src.crud import all_recipe_db, get_recipe_db

NEW_RECIPE: Final[Dict[str, str | int]] = {
    "name": "маргарита",
    "cooking_time": 23,
    "ingredients": "морковь, яйцо",
    "description": "салат",
}


async def all_recipe_db_test() -> List[Dict[str, str | int]]:
    dish = await all_recipe_db()
    dishes: List[Dict[str, str | int]] = [
        {
            "name": d.name,
            "views": d.views,
            "cooking_time": d.cooking_time,
            "id": d.id,
        }
        for d in dish
    ]
    return dishes


async def get_recipe_id_db_test(recipe_id: int) -> Dict[str, str | int]:
    result = await get_recipe_db(recipe_id)
    recipe = {
        "name": result.name,
        "cooking_time": result.cooking_time,
        "ingredients": result.ingredients,
        "description": result.description,
        "id": result.id,
    }
    return recipe
