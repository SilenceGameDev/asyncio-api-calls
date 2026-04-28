from poke_api import Pokemon
import pytest
import pytest_asyncio
import aiohttp

@pytest_asyncio.fixture
async def pokemon() -> Pokemon:
    return Pokemon()


@pytest.mark.asyncio
async def test_can_get_random_pokemon(pokemon: Pokemon):
    async with aiohttp.ClientSession() as session:
        random_pokemon = await pokemon.get_random_pokemon(session)
    assert "forms" in random_pokemon


@pytest.mark.asyncio
async def test_get_random_pokemon_details(pokemon: Pokemon):
    async with aiohttp.ClientSession() as session:
        random_pokemon = await pokemon.get_random_pokemon(session)
    random_pokemon_details = pokemon.get_pokemon_details(random_pokemon)
    assert len(random_pokemon_details) == 3 or len(random_pokemon_details) == 4


@pytest.mark.asyncio
async def test_get_random_pokemon(pokemon):
    async with aiohttp.ClientSession() as session:
        random_pokemon = await pokemon.get_random_pokemon(session)
    assert len(random_pokemon) == 21