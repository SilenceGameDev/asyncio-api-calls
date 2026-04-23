import requests
from logger import logger
from pydantic import BaseModel

class Meal(BaseModel):
    RANDOM_MEAL_ENDPOINT:str = "https://www.themealdb.com/api/json/v1/1/random.php"
    pass

    def get_random_meal(self) -> dict:
        response = requests.get(url=self.RANDOM_MEAL_ENDPOINT)
        logger.info(f"Response code: {response.status_code}")
        response.raise_for_status()

        random_meal = response.json()['meals'][0]
        logger.info(f"Got Random Meal: {random_meal["strMeal"]}")
        return random_meal

    def get_random_meal_details(self, random_meal)-> list:
        meal_name = random_meal["strMeal"]
        meal_instructions = random_meal["strInstructions"]
        meal_image = random_meal["strMealThumb"]
        meal_contents = [
            meal_name,
            meal_image,
            meal_instructions
        ]
        logger.info(f"Got Random Meal Details.")
        return meal_contents

    def get_random_meals(self, amount_of_meals)-> list:
        random_meals = [self.get_random_meal_details(self.get_random_meal()) for _ in range(amount_of_meals)]
        logger.info(f"Got {amount_of_meals} random meals.\n--------------------------")
        return random_meals

# meal_api = Meal()
# meal_api.get_random_meals(7)