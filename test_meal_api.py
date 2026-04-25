from meal import Meal
import pytest
import pytest_asyncio
import aiohttp

@pytest_asyncio.fixture
async def meal():
    return Meal()


@pytest.mark.asyncio
async def test_can_get_random_meal(meal):
    async with aiohttp.ClientSession() as session:
        random_meal = await meal.get_random_meal(session)
    assert "strMeal" in random_meal


@pytest.mark.asyncio
async def test_get_random_meal_details(meal):
    async with aiohttp.ClientSession() as session:
        random_meal = await meal.get_random_meal(session)
    random_meal_details = meal.get_random_meal_details(random_meal)
    assert len(random_meal_details) == 3


@pytest.mark.asyncio
async def test_get_random_meals(meal):
    random_meals = await meal.get_random_meals(5)
    assert len(random_meals) == 5