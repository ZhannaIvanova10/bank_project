# src/processing.py
from typing import Dict, List, Optional


def filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Фильтрует транзакции по статусу"""
    return [t for t in transactions if t.get("state") == state]


def sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]:
    """Сортирует транзакции по дате"""
    return sorted(transactions, key=lambda x: x["date"], reverse=reverse)
