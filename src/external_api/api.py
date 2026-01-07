from typing import Dict, List

import requests


def fetch_transactions(api_url: str) -> List[Dict]:
    """English docstring"""
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return []
