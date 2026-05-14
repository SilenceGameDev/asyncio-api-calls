from logger import logger
from pydantic import BaseModel
import asyncio
import aiohttp
import time
import random

API_REQUEST_LIMIT = 4

class Pokemon(BaseModel):
    pokemon_endpoint:str = "https://pokeapi.co/api/v2/pokemon/"

    async def get_random_pokemon(self, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore) -> dict:
        async with semaphore:
            random_pokemon_endpoint = self.get_random_pokemon_endpoint()
            async with session.get(random_pokemon_endpoint) as response:
                logger.info(f"Response code: {response.status}")
                response.raise_for_status()
                random_pokemon_data = await response.json()
                return random_pokemon_data

    def get_random_pokemon_endpoint(self) -> str:
        random_pokemon_id = random.randint(1, 1025)
        logger.info(f"Random Pokemon ID: {random_pokemon_id}")
        random_pokemon_endpoint = f"{self.pokemon_endpoint}{random_pokemon_id}"
        return random_pokemon_endpoint

    def get_pokemon_details(self, pokemon) -> list:
        pokemon_details = [
            pokemon["species"]["name"].title(),
            pokemon["sprites"]["front_default"],
            pokemon["types"][0]["type"]["name"]
        ]
        if len(pokemon["types"]) > 1:
             pokemon_details.append(pokemon["types"][1]["type"]["name"])
        logger.info(f"Pokemon Details: {pokemon_details}")
        return pokemon_details


    async def get_multiple_random_pokemon(self, amount_of_random_pokemon: int) -> list:
        semaphore = asyncio.Semaphore(API_REQUEST_LIMIT)
        start_time = time.perf_counter()

        async with aiohttp.ClientSession() as session:
            async with asyncio.TaskGroup() as tg:
                tasks = [tg.create_task(self.get_random_pokemon(session,semaphore)) for _ in range(amount_of_random_pokemon)]

        proc_start_time = time.perf_counter()

        multiple_random_pokemon = [self.get_pokemon_details(task.result()) for task in tasks]

        finished_time = time.perf_counter()

        dl_total_time = proc_start_time - start_time
        proc_total_time = finished_time - proc_start_time
        total_time = finished_time - start_time

        print(
            f"\nGot {amount_of_random_pokemon} random pokemon in: {dl_total_time:.2f} seconds. {(dl_total_time / total_time) * 100:.2f}% of total time")
        print(
            f"Got random pokemon details in: {proc_total_time:.2f} seconds. {(proc_total_time / total_time) * 100:.2f}% of total time")
        print(f"\nTotal execution time: {total_time:.2f} seconds. {(total_time / total_time) * 100:.2f}% of total time")

        logger.info(f"Got {amount_of_random_pokemon} random pokemon.\n--------------------------")
        return multiple_random_pokemon

