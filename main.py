from logger import logger
import asyncio
import aiohttp
import time
from aiohttp import ClientResponseError
import random
from flask import Flask, render_template, request
from jinja2 import TemplateNotFound

from meal import Meal
from poke_api import Pokemon
from bible_api import Bible
from currency_api import Currency
from zelda_api import Zelda

app = Flask(__name__)

INDEX_TEMPLATE_NAME: str = "index.html"
LOADING_TEMPLATE_NAME: str = "loading.html"
API_RESULTS_TEMPLATE_NAME: str = "api_results.html"

meal = Meal()
pokemon = Pokemon()
bible = Bible()
currency = Currency()
zelda = Zelda()

@app.errorhandler(404)
def page_not_found(error):
    return "This page doesn't exist"

def try_load_template(template_name: str, **context) -> str:
    try:
        logger.info("Attempting to display home page")
        return render_template(template_name_or_list=template_name, **context)
    except TemplateNotFound:
        logger.error(msg=f"Template: {template_name} not found")
        return page_not_found()

@app.route('/',methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return try_load_template(INDEX_TEMPLATE_NAME)
    else:
        return ""

@app.route('/loading', methods=['GET', 'POST'])
def loading():
    if request.method == 'POST':
        amounts = {
            'meals': int(request.form.get('meals', 5)),
            'pokemon': int(request.form.get('pokemon', 5)),
            'bible': int(request.form.get('bible', 5)),
            'currencies': int(request.form.get('currencies', 5)),
            'zelda': int(request.form.get('zelda', 5)),
        }

        return try_load_template(LOADING_TEMPLATE_NAME, amounts=amounts)
    else:
        return ""

@app.route('/api_results', methods=['GET', 'POST'])
def api_results():
    if request.method == 'POST':
        amounts = {
            'meals': int(request.form.get('meals', 5)),
            'pokemon': int(request.form.get('pokemon', 5)),
            'bible': int(request.form.get('bible', 5)),
            'currencies': int(request.form.get('currencies', 5)),
            'zelda': int(request.form.get('zelda', 5)),
        }

        async def fetch_all():
            async with asyncio.TaskGroup() as tg:
                tasks = [
                    tg.create_task(meal.get_random_meals(amounts['meals'])),
                    tg.create_task(pokemon.get_multiple_random_pokemon(amounts['pokemon'])),
                    tg.create_task(bible.get_random_bible_verses(amounts['bible'])),
                    tg.create_task(currency.get_random_currencies(amounts['currencies'])),
                    tg.create_task(zelda.get_random_entries(amounts['zelda'])),
                ]
            return [task.result() for task in tasks]

        results = asyncio.run(fetch_all())
        return try_load_template(API_RESULTS_TEMPLATE_NAME,
                                 meals=results[0],
                                 pokemon=results[1],
                                 bible_verses=results[2],
                                 currencies=results[3],
                                 zelda_entries=results[4])
    else:
        return try_load_template(API_RESULTS_TEMPLATE_NAME)

if __name__ == "__main__":
    app.run(debug=True)
