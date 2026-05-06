from logger import logger
from pydantic import BaseModel
import asyncio
import aiohttp
import time
from aiohttp import ClientResponseError
import random

class Currency(BaseModel):
    # Currency rates are based off of the US Dollar
    CURRENCY_RATES_ENDPOINT:str = "https://api.frankfurter.dev/v2/rates?base=USD"

    async def get_currency_rates(self, session: aiohttp.ClientSession):
        async with session.get(self.CURRENCY_RATES_ENDPOINT) as response:
            try:
                response.raise_for_status()
                logger.info(f"Response code: {response.status}")
                currency_rates = await response.json()
            except ClientResponseError:
                logger.error(f"Got error: {response.status}")
            return currency_rates

    async def get_currency(self, session: aiohttp.ClientSession, currency_endpoint):
        async with session.get(currency_endpoint) as response:
            try:
                response.raise_for_status()
                logger.info(f"Response code: {response.status}")
                currency = await response.json()
            except ClientResponseError:
                logger.error(f"Got error: {response.status}")
            return currency


    def get_random_currency_rate(self, currency_rates):
        random_currency_rate = random.choice(currency_rates)
        return random_currency_rate

    def get_currency_details(self, rate, currency):
        currency_name = currency["name"]
        currency_iso_code = rate["quote"]
        currency_rate = rate["rate"]
        currency_symbol = currency["symbol"]

        currency_details = [
            currency_name,
            currency_iso_code,
            currency_rate,
            currency_symbol,
        ]
        # not including symbol since it caused errors from encoding.
        logger.info(f"Currency details. Name: {currency_details[0]}. IsoCode: {currency_details[1]}. Rate: {currency_details[2]}")
        return currency_details

    async def get_random_currencies(self, amount_of_currencies):
        async with aiohttp.ClientSession() as session:
            # only need to do this once as it pulls all the currencies
            currency_rates_result = await self.get_currency_rates(session)
            random_currencies = []
            for _ in range(amount_of_currencies):
                random_currency_rate = self.get_random_currency_rate(currency_rates_result)
                currency_iso_code = random_currency_rate["quote"]
                currency_endpoint = f"https://api.frankfurter.dev/v2/currency/{currency_iso_code}"
                currency_result = await self.get_currency(session, currency_endpoint)
                random_currencies.append(self.get_currency_details(random_currency_rate, currency_result))

        logger.info(f"Got {amount_of_currencies} random currencies.\n--------------------------")
        return random_currencies


# used to quickly test the api
# async def main():
#     currency = Currency()
#     async with aiohttp.ClientSession() as session:
#         currency_rates_result = await currency.get_currency_rates(session)  # await not asyncio.run()
#         random_currency_rate = currency.get_random_currency_rate(currency_rates_result)
#         currency.currency_iso_code = random_currency_rate["quote"]
#         currency.currency_endpoint = f"https://api.frankfurter.dev/v2/currency/{currency.currency_iso_code}"
#         currency_result = await currency.get_currency(session)
#         currency_details = currency.get_currency_details(random_currency_rate, currency_result)
#         print(currency_details)
#
# if __name__ == "__main__":
#     asyncio.run(main())  # asyncio.run() goes here at the entry point only

def main():
    currency = Currency()
    asyncio.run(currency.get_random_currencies(amount_of_currencies=5))

if __name__ == "__main__":
    main()