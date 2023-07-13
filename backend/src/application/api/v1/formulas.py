from src.application.db_commands import (
    get_reward_block_or_404,
    get_difficulty_or_404,
    get_maintenance_coast_or_404,
    get_btc_price_or_404,
    get_th_rental_cost_or_404
)


def calculate_income_btc(btc_amount: float = 1):
    H = btc_amount * 10 ** 12
    t = 86400  # секунд в сутках
    R = get_reward_block_or_404()
    D = get_difficulty_or_404()
    return (t * R.reward_block * H) / (D.difficulty * 2 ** 32)


def calculate_income_usd(btc_amount: float):
    D = calculate_income_btc()
    C = btc_amount
    B = get_btc_price_or_404()
    S = get_maintenance_coast_or_404()
    return (D * C * B.price) - (S.coast * C)


def calculate_contract_price(contract_data: dict):
    hashrate_count = contract_data.get('hashrate')
    contract_start = contract_data.get('contract_start')
    contract_end = contract_data.get('contract_end')
    mining_period = (contract_end - contract_start).total_seconds()
    th_rental_cost = get_th_rental_cost_or_404()
    return hashrate_count * th_rental_cost.cost * mining_period
