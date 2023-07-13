from django.shortcuts import get_object_or_404
from src.application.models import (
    Difficulty,
    Reward,
    MaintenanceCost,
    BtcPrice,
    RentalThCost
)


def update_or_create_difficulty(difficulty: int):
    Difficulty.objects.update_or_create(
        id='difficulty', defaults={'difficulty': difficulty}
    )


def update_or_create_reward(blocks: int):
    reward_block = 50 / 2 ** (blocks // 210_000)
    Reward.objects.update_or_create(
        id='reward_block', defaults={'reward_block': reward_block}
    )


def update_or_create_btc_price(btc_price: float):
    BtcPrice.objects.update_or_create(
        id='btc_price', defaults={'price': btc_price}
    )


def get_difficulty_or_404():
    return get_object_or_404(
        Difficulty, id='difficulty'
    )


def get_reward_block_or_404():
    return get_object_or_404(
        Reward, id='reward_block'
    )


def get_maintenance_coast_or_404():
    return get_object_or_404(
        MaintenanceCost, id='maintenance_cost'
    )


def get_btc_price_or_404():
    return get_object_or_404(
        BtcPrice, id='btc_price'
    )


def get_th_rental_cost_or_404():
    return get_object_or_404(
        RentalThCost, id='th_rental_cost'
    )
