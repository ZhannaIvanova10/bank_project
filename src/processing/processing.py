from datetime import datetime
from typing import List, Dict, Any


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу

    :param transactions: Список транзакций
    :param state: Статус для фильтрации (по умолчанию "EXECUTED")
    :return: Отфильтрованный список
    """
    return [t for t in transactions if t.get("state", "").upper() == state.upper()]


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате

    :param transactions: Список транзакций
    :param reverse: Сортировка по убыванию (по умолчанию True)
    :return: Отсортированный список
    """
    return sorted(
        transactions,
        key=lambda x: datetime.fromisoformat(x["date"]),
        reverse=reverse
    )
