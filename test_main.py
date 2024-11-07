from typing import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database import Base
from main import app, get_db


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Start a test database session."""
    test_db_url: str = "sqlite+aiosqlite:///./test_app.db"
    engine = create_async_engine(test_db_url, echo=True)
    Session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    session = Session()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield session
    await session.close()


@pytest.fixture()
def test_app(db_session: AsyncSession):
    """Create a test app with overridden dependencies."""
    app.dependency_overrides[get_db] = lambda: db_session
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture()
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create an http client."""
    async with AsyncClient(app=test_app, base_url="http://localhost:8000") as client:
        yield client


recipe_in: dict = {
    "title": "test_title",
    "description": "test_description",
    "ingredients": "test_ingredients",
    "cooking_time": 1.1,
}
cur_prefix: int = 0


def _add_prefix():
    """Функция добавляет префикс к полям self.test_detailed_recipe,
    чтобы добавлять уникальные значение при тестировании
    """
    global cur_prefix
    prefix: str = f"_{cur_prefix}"
    recipe_in["title"] += prefix
    recipe_in["description"] += prefix
    recipe_in["ingredients"] += prefix
    cur_prefix += 1


@pytest.mark.asyncio
async def test_add_new_recipe_and_return_same_recipe(client):
    """Unit тест. Проверяет, что при отправке корректной формы,
    возвращает отправленный json, код 200"""
    _add_prefix()
    response = await client.post("/recipes", json=recipe_in)
    assert response.status_code == 200

    response_json = response.json()
    response_json.pop("recipe_id")
    assert response_json == recipe_in


@pytest.mark.asyncio
async def test_added_recipe_in_bd(client):
    """Unit тест. Проверяет, что при отправке корректной формы,
    рецепт сохраняется в бд"""
    _add_prefix()
    # Отправим рецепт в бд через POST
    response_post = await client.post("/recipes", json=recipe_in)
    response_post_json = response_post.json()
    recipe_id: int = response_post_json.get("recipe_id")

    # получим рецепт из бд через GET и id рецепта
    response_get = await client.get(f"/recipes/{recipe_id}")
    response_get_json = response_get.json()
    assert response_post_json == response_get_json


@pytest.mark.asyncio
async def test_negative_post_invalid_form(client):
    """Негативный unit тест. Проверка отправки невалидной формы"""
    response = await client.post("/recipes", json={"smth": "smb"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_negative_recipe_not_found(client):
    """Негативный unit тест.
    Проверяет, что если запросить рецепт по id,
    которого нет в бд, то вернет 404 код"""
    response = await client.get("/recipes/1000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_all_recipes(client):
    """Unit тест.
    Проверяет, что endpoint GET /recipes работает
    и возвращает 200 код"""
    response = await client.get("/recipes")
    assert response.status_code == 200
