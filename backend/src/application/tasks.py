import os
import requests

from dotenv import load_dotenv
from config.celery import app
from src.application.db_commands import (
    change_or_create_difficulty,
    change_or_create_reward
)


load_dotenv()

LAST_BLOCK_DATA = os.environ.get('LAST_BLOCK_DATA')


@app.task
def get_orders_for_save_in_db():
    try:
        resonse = requests.get(url=LAST_BLOCK_DATA)
        if resonse.status_code == 200:
            block_data = resonse.json().get('data')
            difficulty = block_data.get('difficulty')
            reward = block_data.get('reward_block')
            if difficulty:
                change_or_create_difficulty(difficulty=difficulty)
            if reward:
                change_or_create_reward(reward=reward)
    except Exception:
        return None
