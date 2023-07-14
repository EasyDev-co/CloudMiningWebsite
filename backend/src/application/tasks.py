import os
import requests

from dotenv import load_dotenv
from config.celery import app
from src.application.db_commands import (
    update_or_create_difficulty,
    update_or_create_reward,
    update_or_create_btc_price,
    update_or_create_eth_price
)


load_dotenv()

LAST_BLOCK_DATA = os.environ.get('LAST_BLOCK_DATA')
BTC_DATA_TOKEN = os.environ.get('BTC_DATA_TOKEN')

BTC_TO_USD = os.environ.get('BTC_TO_USD')
ETH_TO_USD = os.environ.get('ETH_TO_USD')


@app.task
def save_new_block_data_in_db():
    try:
        resonse = requests.post(
            url=LAST_BLOCK_DATA,
            headers={
                'x-api-key': BTC_DATA_TOKEN
            },
            json={
                "jsonrpc": "2.0",
                "method": "getblockchaininfo",
                "params": [],
                "id": "getblock.io"
            }
        )
        if resonse.status_code == 200:
            block_data = resonse.json().get('result')
            difficulty = block_data.get('difficulty')
            blocks = block_data.get('blocks')
            if difficulty:
                update_or_create_difficulty(difficulty=difficulty)
            if blocks:
                update_or_create_reward(blocks=blocks)
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


@app.task
def save_new_eth_price_in_db():
    try:
        resonse = requests.get(url=ETH_TO_USD)
        if resonse.status_code == 200:
            eth_price = resonse.json().get('price')
            if eth_price:
                update_or_create_eth_price(eth_price=eth_price)
    except Exception:
        return None
