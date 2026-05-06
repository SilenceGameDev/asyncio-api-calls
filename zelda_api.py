from logger import logger
from pydantic import BaseModel
import asyncio
import aiohttp
import time
from aiohttp import ClientResponseError
import random

class Zelda(BaseModel):
    pass

    async def get_random_entry(self, session: aiohttp.ClientSession):
        random_entry = random.randint(1,389)
        logger.info(f"Random entry: {random_entry}")
        hyrule_compendium_api_endpoint = f"https://botw-compendium.herokuapp.com/api/v3/compendium/entry/{random_entry}"
        async with session.get(hyrule_compendium_api_endpoint) as response:
            try:
                response.raise_for_status()
                logger.info(f"Response code: {response.status}")
                random_entry_result = await response.json()
            except ClientResponseError:
                logger.error(f"Got error: {response.status}")
            return random_entry_result

    def get_entry_details(self, entry):
        entry_name = entry["data"]["name"]
        entry_image = entry["data"]["image"]
        entry_category = entry["data"]["category"]

        entry_details = [
            entry_name,
            entry_image,
            entry_category
        ]
        logger.info(f"Entry details: {entry_details}")
        return entry_details

    async def get_random_entries(self, amount_of_entries:int):
        start_time = time.perf_counter()
        async with aiohttp.ClientSession() as session:
            async with asyncio.TaskGroup() as tg:
                tasks = [tg.create_task(self.get_random_entry(session)) for _ in range(amount_of_entries)]

        proc_start_time = time.perf_counter()

        random_entries = [self.get_entry_details(task.result()) for task in tasks]

        finished_time = time.perf_counter()

        dl_total_time = proc_start_time - start_time
        proc_total_time = finished_time - proc_start_time
        total_time = finished_time - start_time

        print(
            f"\nGot {amount_of_entries} random entries in: {dl_total_time:.2f} seconds. {(dl_total_time / total_time) * 100:.2f}% of total time")
        print(
            f"Got random entry details in: {proc_total_time:.2f} seconds. {(proc_total_time / total_time) * 100:.2f}% of total time")
        print(f"\nTotal execution time: {total_time:.2f} seconds. {(total_time / total_time) * 100:.2f}% of total time")

        logger.info(f"Got {amount_of_entries} random entries.\n--------------------------")
        return random_entries

def main():
    zelda = Zelda()
    asyncio.run(zelda.get_random_entries(amount_of_entries=5))

if __name__ == "__main__":
    main()

# # used to quickly test the api
# async def main():
#     zelda = Zelda()
#     async with aiohttp.ClientSession() as session:
#         result = await zelda.get_random_entry(session)  # await not asyncio.run()
#         entry_details = zelda.get_entry_details(result)
#         print(entry_details)
#
# if __name__ == "__main__":
#     asyncio.run(main())  # asyncio.run() goes here at the entry point only