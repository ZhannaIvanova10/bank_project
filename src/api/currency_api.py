from typing import Dict, Union

import requests

CURRENCY_RATES = {"USD": 75.0, "EUR": 85.0, "GBP": 95.0}


def get_currency_rate(currency: str) -> float:
    """Get current exchange rate for currency"""
    currency = currency.upper()
    return CURRENCY_RATES.get(currency, 1.0)


def convert_to_rub(amount: float, currency: str) -> float:
    """Convert amount to rubles"""
    rate = get_currency_rate(currency)
    return round(amount * rate, 2)


def get_all_rates() -> Dict[str, float]:
    """Get all available currency rates"""
    return CURRENCY_RATES.copy()
