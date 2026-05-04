from bible_api import Bible
import pytest
import pytest_asyncio
import aiohttp

@pytest_asyncio.fixture
async def bible():
    return Bible()


@pytest.mark.asyncio
async def test_can_get_random_bible_verse(bible):
    async with aiohttp.ClientSession() as session:
        random_verse = await bible.get_random_bible_verse(session)
    assert "book" in random_verse["random_verse"]


@pytest.mark.asyncio
async def test_get_random_bible_verse_details(bible):
    async with aiohttp.ClientSession() as session:
        random_verse = await bible.get_random_bible_verse(session)
    random_verse_details = bible.get_random_bible_verse_details(random_verse)
    assert len(random_verse_details) == 4


@pytest.mark.asyncio
async def test_get_random_bible_verses(bible):
    random_verse = await bible.get_random_bible_verses(5)
    assert len(random_verse) == 5