from src.application.models import Difficulty, Reward


def change_or_create_difficulty(difficulty: int):
    diff = Difficulty.objects.first()
    if diff:
        diff.difficulty = difficulty
        diff.save()
    else:
        Difficulty.objects.create(difficulty=difficulty)


def change_or_create_reward(reward: int):
    reward_block = round((reward / (10 ** (len(str(reward)) - 1))), 2)
    rew = Reward.objects.first()
    if rew:
        rew.reward_block = reward_block
        rew.save()
    else:
        Reward.objects.create(reward_block=reward_block)


def get_difficulty():
    return Difficulty.objects.first()


def get_reward_block():
    return Reward.objects.first()
