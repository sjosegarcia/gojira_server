from .model_schema import Model
from typing import Optional
from datetime import datetime


class MarketData(Model):
    ath: float
    atl: float
    change_24h: float
    change_percentage_24h: float
    change_percentage_7d: float
    change_percentage_14d: float
    change_percentage_30d: float
    init_supply: int
    max_supply: int
    total_supply: float
    current_supply: float
    daily_volume: float
    market_cap: float
    fully_diluted_valuation: float
    current_liquidity: float
    zil_reserve: float
    token_reserve: float


class TokenRewards(Model):
    id: int
    created_at: datetime
    updated_at: datetime
    type: str
    amount: float
    max_individual_amount: float
    reward_token_id: int
    reward_token_address: str
    reward_token_symbol: str
    frequency: int
    frequency_type: str
    excluded_addresses: str
    contract_address: str
    contract_state: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]


class GenericTokenInfo(Model):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    symbol: str
    address_bech32: str
    icon: str
    decimals: int
    website: Optional[str]
    whitepaper: Optional[str]
    init_supply: float
    max_supply: float
    total_supply: float
    current_supply: float
    daily_volume: float
    current_liquidity: float
    supply_skip_addresses: str
    viewblock_score: int


class TokenInfo(Model):
    name: str
    symbol: str
    address_bech32: str
    decimals: int
    website: str
    whitepaper: str
    viewblock_score: int
    listed: bool
    current_supply: float
    daily_volume: float
    supply_skip_addresses: str
    market_cap: float
    rate: float
    rate_usd: float
    market_data: MarketData
    rewards: list[TokenRewards]
