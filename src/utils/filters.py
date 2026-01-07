from typing import List, Dict, Any, Optional
from datetime import datetime


def filter_by_status(data: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу.

    Args:
        data: Список словарей с данными о банковских операциях
        status: Статус для фильтрации

    Returns:
        Отфильтрованный список транзакций
    """
    if not data:
        return []

    status_lower = status.lower()
    return [transaction for transaction in data
            if transaction.get('state', '').lower() == status_lower]


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.

    Args:
        data: Список словарей с данными о банковских операциях
        reverse: Если True - сортировка по убыванию, иначе по возрастанию

    Returns:
        Отсортированный список транзакций
    """
    if not data:
        return []

    def get_date(transaction: Dict[str, Any]) -> datetime:
        date_str = transaction.get('date', '')
        try:
            return datetime.fromisoformat(date_str.replace('Z', ''))
        except (ValueError, AttributeError):
            return datetime.min

    return sorted(data, key=get_date, reverse=reverse)


def filter_by_currency(data: List[Dict[str, Any]], currency: str = 'RUB') -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по валюте.

    Args:
        data: Список словарей с данными о банковских операциях
        currency: Код валюты для фильтрации

    Returns:
        Отфильтрованный список транзакций
    """
    if not data:
        return []

    currency_upper = currency.upper()
    return [transaction for transaction in data
            if transaction.get('operationAmount', {}).get('currency', {}).get('code', '').upper() == currency_upper]