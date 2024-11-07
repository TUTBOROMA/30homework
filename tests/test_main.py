import asyncio
from asyncio import AbstractEventLoop
from random import randint
from typing import AsyncGenerator, List, Dict, Iterator

import pytest
from httpx import ASGITransport, AsyncClient, Response

from .database_test import (
    all_recipe_db_test,
    get_recipe_id_db_test,
    NEW_RECIPE,
)
from src.crud import delete_recipe_by_id_test
from src.main import app


@pytest.mark.asyncio(scope="session")
def event_loop() -> Iterator[AbstractEventLoop]:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# client: TestClient = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


async def test_get_recipes(ac: AsyncClient):
    dishes: List[Dict[str, str | int]] = await all_recipe_db_test()
    response: Response = await ac.get("/recipes")

    assert response.status_code == 200
    assert response.json() == dishes


async def test_get_recipes_negative(ac: AsyncClient):
    dishes: List[Dict[str, str | int]] = await all_recipe_db_test()
    dishes[randint(1, len(dishes))]["cooking_time"] = 0
    response: Response = await ac.get("/recipes")

    assert response.status_code == 200
    assert response.json() != dishes


async def test_cooking_time_should_be_more_than_0_minutes(ac: AsyncClient):
    response: Response = await ac.get("/recipes")
    data: List[Dict[str, str | int]] = response.json()

    assert response.status_code == 200
    for d in data:
        assert d["cooking_time"] > 0


async def test_get_recipes_data_type_checking(ac: AsyncClient):
    # dishes: List[Dict[str, str | int]] = await all_recipe_db_test()
    response: Response = await ac.get("/recipes")

    assert response.status_code == 200
    assert response.json().__class__ is list


async def test_get_recipe_by_id(ac: AsyncClient):
    recipe_id: int = 2
    recipe = await get_recipe_id_db_test(recipe_id)
    response: Response = await ac.get(f"/recipes/{recipe_id}")

    assert response.status_code == 200
    assert response.json() == recipe


async def test_get_recipe_by_id_negative(ac: AsyncClient):
    recipe_id: int = 2
    recipe = await get_recipe_id_db_test(recipe_id)
    recipe["name"] = ""
    response: Response = await ac.get(f"/recipes/{recipe_id}")

    assert response.status_code == 200
    assert response.json() != recipe


async def test_get_recipe_by_non_existent_id(ac: AsyncClient):
    dishes: List[Dict[str, str | int]] = await all_recipe_db_test()
    max_id: int = max(d["id"] for d in dishes)
    recipe_non_existent_id: int = max_id + randint(1, 10)
    response = await ac.get(f"/recipes/{recipe_non_existent_id}")

    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Recipe by {recipe_non_existent_id} not found!"
    }


async def test_get_recipe_by_id__data_type_checking(ac: AsyncClient):
    recipe_id: int = 2
    response: Response = await ac.get(f"/recipes/{recipe_id}")

    assert response.status_code == 200
    assert response.json().__class__ is dict


async def test_new_creat_recipe_negative(ac: AsyncClient):
    response = await ac.post("/recipes", json=NEW_RECIPE)
    data = response.json()

    assert response.status_code == 201
    assert response.json() != NEW_RECIPE
    await delete_recipe_by_id_test(data["id"])


async def test_new_creat_recipe(ac: AsyncClient):
    response = await ac.post("/recipes", json=NEW_RECIPE)
    data = response.json()
    NEW_RECIPE["id"] = data["id"]

    assert response.status_code == 201
    assert response.json() == NEW_RECIPE
    await delete_recipe_by_id_test(data["id"])


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-vxs"])
# Run pytest -vs
