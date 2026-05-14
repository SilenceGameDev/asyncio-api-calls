from time import sleep

from aiohttp import ClientResponseError
from logger import logger
from pydantic import BaseModel
import asyncio
import aiohttp
import time

API_REQUEST_LIMIT = 4

default_verse = {"reference":"John 3:16","verses":[{"book_id":"JHN","book_name":"John","chapter":3,"verse":16,"text":"\nFor God so loved the world, that he gave his one and only Son, that whoever believes in him should not perish, but have eternal life.\n\n"}],"text":"\nFor God so loved the world, that he gave his one and only Son, that whoever believes in him should not perish, but have eternal life.\n\n","translation_id":"web","translation_name":"World English Bible","translation_note":"Public Domain"}

class Bible(BaseModel):
    BIBLE_ENDPOINT:str = "https://bible-api.com/data/kjv/random"

    async def get_random_bible_verse(self, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore)->str:
        async with semaphore:
            async with session.get(self.BIBLE_ENDPOINT) as response:
                try:
                    response.raise_for_status()
                    logger.info(f"Response code: {response.status}")
                    bible_verse = await response.json()
                except ClientResponseError:
                    logger.error(f"Got error: {response.status}. Setting default verse")
                    bible_verse = default_verse
                except UnboundLocalError:
                    logger.error(f"Got UnboundLocalError: {response.status}. Setting default verse")
                    bible_verse = default_verse
                return bible_verse

    def get_random_bible_verse_details(self, random_bible_verse):
        try:
            book = random_bible_verse["random_verse"]["book"]
            chapter = random_bible_verse["random_verse"]["chapter"]
            verse = random_bible_verse["random_verse"]["verse"]
            text =random_bible_verse["random_verse"]["text"]
        except KeyError:
            book = "John"
            chapter = "3"
            verse = "16"
            text = default_verse["verses"][0]["text"]
        bible_verse_details = [
            book,
            chapter,
            verse,
            text
        ]
        logger.info(f"Book: {bible_verse_details[0]} Chapter: {bible_verse_details[1]} Verse {bible_verse_details[2]} Text {bible_verse_details[3]}")
        return bible_verse_details

    async def get_random_bible_verses(self, amount_of_verses)->list:
        semaphore = asyncio.Semaphore(API_REQUEST_LIMIT)
        start_time = time.perf_counter()
        async with aiohttp.ClientSession() as session:
            async with asyncio.TaskGroup() as tg:
                tasks = [tg.create_task(self.get_random_bible_verse(session,semaphore)) for _ in range(amount_of_verses)]

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

# # used to quickly test the api
# async def main():
#     bible = Bible()
#     result = await bible.get_random_bible_verses(25)
#     print(result)
#
# if __name__ == "__main__":
#     asyncio.run(main())