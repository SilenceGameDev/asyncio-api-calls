from aiohttp import ClientResponseError
from logger import logger
from pydantic import BaseModel
import asyncio
import aiohttp
import time

class Bible(BaseModel):
    BIBLE_ENDPOINT:str = "https://bible-api.com/data/kjv/random"

    async def get_random_bible_verse(self, session: aiohttp.ClientSession)->str:
        async with session.get(self.BIBLE_ENDPOINT) as response:
            try:
                response.raise_for_status()
                logger.info(f"Response code: {response.status}")
                bible_verse = await response.json()
            except ClientResponseError:
                logger.error(f"Got error: {response.status}")
            return bible_verse


    def get_random_bible_verse_details(self, random_bible_verse):
        bible_verse_details = [
            random_bible_verse["random_verse"]["book"],
            random_bible_verse["random_verse"]["chapter"],
            random_bible_verse["random_verse"]["verse"],
            random_bible_verse["random_verse"]["text"]
        ]

        logger.info(f"Book: {bible_verse_details[0]} Chapter: {bible_verse_details[1]} Verse {bible_verse_details[2]} Text {bible_verse_details[3]}")
        return bible_verse_details


    async def get_random_bible_verses(self, amount_of_verses)->list:
        start_time = time.perf_counter()
        async with aiohttp.ClientSession() as session:
            async with asyncio.TaskGroup() as tg:
                tasks = [tg.create_task(self.get_random_bible_verse(session)) for _ in range(amount_of_verses)]

        proc_start_time = time.perf_counter()

        random_bible_verses = [self.get_random_bible_verse_details(task.result()) for task in tasks]

        finished_time = time.perf_counter()

        dl_total_time = proc_start_time - start_time
        proc_total_time = finished_time - proc_start_time
        total_time = finished_time - start_time

        print(
            f"\nGot {amount_of_verses} random bible verses in: {dl_total_time:.2f} seconds. {(dl_total_time / total_time) * 100:.2f}% of total time")
        print(
            f"Got random bible verse details in: {proc_total_time:.2f} seconds. {(proc_total_time / total_time) * 100:.2f}% of total time")
        print(f"\nTotal execution time: {total_time:.2f} seconds. {(total_time / total_time) * 100:.2f}% of total time")

        logger.info(f"Got {amount_of_verses} random bible verses.\n--------------------------")
        return random_bible_verses


def main():
    bible = Bible()
    asyncio.run(bible.get_random_bible_verses(amount_of_verses=5))

if __name__ == "__main__":
    main()

# used to quickly test the api
# async def main():
#     bible = Bible()
#     async with aiohttp.ClientSession() as session:
#         result = await bible.get_bible_verse(session)  # await not asyncio.run()
#         print(result)
#
# if __name__ == "__main__":
#     asyncio.run(main())  # asyncio.run() goes here at the entry point only