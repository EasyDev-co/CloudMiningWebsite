from src.application.models import Difficulty, Reward, MaintenanceCost
from django.shortcuts import get_object_or_404


def change_or_create_difficulty(difficulty: int):
    Difficulty.objects.update_or_create(
        id='difficulty', defaults={'difficulty': difficulty}
    )


def change_or_create_reward(reward: int):
    reward_block = round((reward / (10 ** (len(str(reward)) - 1))), 2)
    Reward.objects.update_or_create(
        id='reward_block', defaults={'reward_block': reward_block}
    )


def get_difficulty():
    return get_object_or_404(
        Difficulty, id='difficulty'
    )


def get_reward_block():
    return get_object_or_404(
        Reward, id='reward_block'
    )


def get_maintenance_coast():
    return get_object_or_404(
        MaintenanceCost, id='maintenance_cost'
    )
