import os
import requests

from dotenv import load_dotenv
from config.celery import app
from src.application.db_commands import (
    update_or_create_difficulty,
    update_or_create_reward,
    update_or_create_btc_price
)


load_dotenv()

LAST_BLOCK_DATA = os.environ.get('LAST_BLOCK_DATA')
BTC_TO_USD = os.environ.get('BTC_TO_USD')


@app.task
def save_new_block_data_in_db():
    try:
        resonse = requests.get(url=LAST_BLOCK_DATA)
        if resonse.status_code == 200:
            block_data = resonse.json().get('data')
            difficulty = block_data.get('difficulty')
            reward = block_data.get('reward_block')
            if difficulty:
                update_or_create_difficulty(difficulty=difficulty)
            if reward:
                update_or_create_reward(reward=reward)
    except Exception:
        return None


@app.task
def save_new_btc_price_in_db():
    try:
        resonse = requests.get(url=BTC_TO_USD)
        if resonse.status_code == 200:
            btc_price = resonse.json().get('price')
            if btc_price:
                update_or_create_btc_price(btc_price=btc_price)
    except Exception:
        return None
