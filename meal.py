from logger import logger
from pydantic import BaseModel
import asyncio
import aiohttp
import time

class Meal(BaseModel):
    RANDOM_MEAL_ENDPOINT:str = "https://www.themealdb.com/api/json/v1/1/random.php"


    async def get_random_meal(self, session: aiohttp.ClientSession) -> dict:
        async with session.get(url=self.RANDOM_MEAL_ENDPOINT) as response:
            logger.info(f"Response code: {response.status}")
            response.raise_for_status()
            data = await response.json()
            random_meal = data['meals'][0]
            logger.info(f"Got Random Meal: {random_meal['strMeal']}")
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
        logger.info(f"Got Random Meal Details from {meal_name}.")
        return meal_contents

    async def get_random_meals(self, amount_of_meals) -> list:
        start_time = time.perf_counter()

        async with aiohttp.ClientSession() as session:
            async with asyncio.TaskGroup() as tg:
                tasks = [tg.create_task(self.get_random_meal(session)) for _ in range(amount_of_meals)]

        proc_start_time = time.perf_counter()

        random_meals = [self.get_random_meal_details(task.result()) for task in tasks]

        finished_time = time.perf_counter()

        dl_total_time = proc_start_time - start_time
        proc_total_time = finished_time - proc_start_time
        total_time = finished_time - start_time

        print(
            f"\nGot {amount_of_meals} random meals in: {dl_total_time:.2f} seconds. {(dl_total_time / total_time) * 100:.2f}% of total time")
        print(
            f"Got random meal details in: {proc_total_time:.2f} seconds. {(proc_total_time / total_time) * 100:.2f}% of total time")
        print(f"\nTotal execution time: {total_time:.2f} seconds. {(total_time / total_time) * 100:.2f}% of total time")

        logger.info(f"Got {amount_of_meals} random meals.\n--------------------------")
        return random_meals

def main():
    meal_api = Meal()
    asyncio.run(meal_api.get_random_meals(15))

if __name__ == "__main__":
    main()