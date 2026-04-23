from meal_api import Meal
import pytest

@pytest.fixture
def meal():
    return Meal()


def test_can_get_random_meal(meal):
    random_meal = meal.get_random_meal()
    assert random_meal.__contains__("strMeal")

def test_get_random_meal_details(meal):
    random_meal = meal.get_random_meal()
    random_meal_details = meal.get_random_meal_details(random_meal)
    assert len(random_meal_details) == 3

def test_get_random_meals(meal):
    random_meals = meal.get_random_meals(5)
    assert len(random_meals) == 5