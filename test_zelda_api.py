from zelda_api import Zelda
import pytest
import pytest_asyncio
import aiohttp

@pytest_asyncio.fixture
async def zelda() -> Zelda:
    return Zelda()


@pytest.mark.asyncio
async def test_get_random_entry(zelda: Zelda):
    async with aiohttp.ClientSession() as session:
        random_entry = await zelda.get_random_entry(session)
    assert "name" in random_entry["data"]


@pytest.mark.asyncio
async def test_get_entry_details(zelda: Zelda):
    async with aiohttp.ClientSession() as session:
        random_entry = await zelda.get_random_entry(session)
    random_entry_details = zelda.get_entry_details(random_entry)
    assert len(random_entry_details) == 3


@pytest.mark.asyncio
async def test_get_random_entries(zelda):
    random_entries = await zelda.get_random_entries(5)
    assert len(random_entries) == 5