from logger import logger
import asyncio
import aiohttp
import time
from aiohttp import ClientResponseError
import random

from meal import Meal
from poke_api import Pokemon
from bible_api import Bible
from currency_api import Currency
from zelda_api import Zelda

meal = Meal()
pokemon = Pokemon()
bible = Bible()
currency = Currency()
zelda = Zelda()

async def main():
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(meal.get_random_meals(10)),
                 tg.create_task(pokemon.get_multiple_random_pokemon(5)),
                 tg.create_task(bible.get_random_bible_verses(5)),
                 tg.create_task(currency.get_random_currencies(5)),
                 tg.create_task(zelda.get_random_entries(5)),
                 ]

        return tasks

if __name__ == "__main__":
    results = asyncio.run(main())
    print("Done All tasks")
    print(results[1].result()[2])
