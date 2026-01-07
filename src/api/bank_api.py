import os
from typing import Optional

import requests


def get_currency_rate(currency: str) -> Optional[float]:
    """English docstring"""
    if currency == "RUB":
        return 1.0

    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key:
        raise ValueError("API key not found")

    try:
        response = requests.get(
            f"https://api.apilayer.com/exchangerates_data/latest?base={currency}&symbols=RUB",
            headers={"apikey": api_key},
        )
        response.raise_for_status()
        return response.json()["rates"]["RUB"]
    except requests.RequestException:
        return None
