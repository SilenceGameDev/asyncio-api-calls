from currency_api import Currency
import pytest
import pytest_asyncio
import aiohttp

@pytest_asyncio.fixture
async def currency() -> Currency:
    return Currency()


@pytest.mark.asyncio
async def test_get_currency_rates(currency: Currency):
    async with aiohttp.ClientSession() as session:
        currency_rates = await currency.get_currency_rates(session)
    assert len(currency_rates) == 163

@pytest.mark.asyncio
async def test_get_currency(currency: Currency):
    currency_endpoint = "https://api.frankfurter.dev/v2/currency/USD"
    async with aiohttp.ClientSession() as session:
        single_currency = await currency.get_currency(session, currency_endpoint)
    assert "symbol" in single_currency

@pytest.mark.asyncio
async def test_get_random_currency_rate(currency: Currency):
    async with aiohttp.ClientSession() as session:
        # only need to do this once as it pulls all the currencies
        currency_rates_result = await currency.get_currency_rates(session)
    random_currency_rate = currency.get_random_currency_rate(currency_rates_result)
    assert "quote" in random_currency_rate

@pytest.mark.asyncio
async def test_currency_details(currency: Currency):
    currency_endpoint = "https://api.frankfurter.dev/v2/currency/USD"
    async with aiohttp.ClientSession() as session:
        currency_rates_result = await currency.get_currency_rates(session)
        random_currency_rate = currency.get_random_currency_rate(currency_rates_result)
        currency_result = await currency.get_currency(session, currency_endpoint)
        currency_details = currency.get_currency_details(random_currency_rate, currency_result)
    assert "United States Dollar" in currency_details

@pytest.mark.asyncio
async def test_get_random_currencies(currency: Currency):
    async with aiohttp.ClientSession() as session:
        currency_rates_result = await currency.get_currency_rates(session)
        random_currencies = []
        for _ in range(5):
            random_currency_rate = currency.get_random_currency_rate(currency_rates_result)
            currency_iso_code = random_currency_rate["quote"]
            currency_endpoint = f"https://api.frankfurter.dev/v2/currency/{currency_iso_code}"
            currency_result = await currency.get_currency(session, currency_endpoint)
            random_currencies.append(currency.get_currency_details(random_currency_rate, currency_result))
        assert len(random_currencies) == 5
