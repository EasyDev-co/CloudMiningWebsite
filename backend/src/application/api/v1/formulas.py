from src.application.db_commands import (
    get_reward_block,
    get_difficulty
)


def calculate_income_btc(mining_period: int, btc_amount: float = 1):
    H = btc_amount * 10 ** 12
    t = mining_period
    R = get_reward_block()
    D = get_difficulty()
    return (t * R * H) / (D * 2 ** 32)


def calculate_income_usd(btc_amount: float, mining_period: int):
    D = calculate_income_btc(mining_period)
    C = btc_amount
    B = 27939.3  # нужно парсить Binance
    S = 12  # указывается при заключении контракта со стороны администратора сайта
    return (D * C * B) - (S * C)
