from src.application.db_commands import (
    get_reward_block_or_404,
    get_difficulty_or_404,
    get_maintenance_coast_or_404
)


def calculate_income_btc(mining_period: int, btc_amount: float = 1):
    H = btc_amount * 10 ** 12
    t = mining_period
    R = get_reward_block_or_404()
    D = get_difficulty_or_404()
    return (t * R.reward_block * H) / (D.difficulty * 2 ** 32)


def calculate_income_usd(btc_amount: float, mining_period: int):
    D = calculate_income_btc(mining_period)
    C = btc_amount
    B = 27939.3  # нужно парсить Binance
    S = get_maintenance_coast_or_404()
    return (D * C * B) - (S.coast * C)
