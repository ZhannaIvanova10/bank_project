"""Модуль для фильтрации транзакций."""
from datetime import datetime
from typing import List, Dict, Any


def filter_by_status(data: List[Dict[str, Any]], status: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу.
    
    Args:
        data: Список транзакций
        status: Статус для фильтрации (EXECUTED, CANCELED, PENDING)
    Returns:
        Отфильтрованный список транзакций
    """
    if not data:
        return []
    
    filtered = []
    for transaction in data:
        if transaction.get('state') == status:
            filtered.append(transaction)
    
    return filtered


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.
    
    Args:
        data: Список транзакций
        reverse: Если True - сортировка по убыванию, False - по возрастанию
        
    Returns:
        Отсортированный список транзакций
    """
    def get_date(transaction: Dict[str, Any]) -> datetime:
        """Вспомогательная функция для получения даты из транзакции."""
        date_str = transaction.get('date', '')
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return datetime.min
        except (ValueError, AttributeError):
            return datetime.min
    
    return sorted(data, key=get_date, reverse=reverse)


def filter_by_currency(data: List[Dict[str, Any]], currency: str = "RUB") -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по валюте.
    
    Args:
        data: Список транзакций
        currency: Код валюты для фильтрации
        
    Returns:
        Отфильтрованный список транзакций
    """
    if not data:
        return []
    filtered = []
    for transaction in data:
        operation_amount = transaction.get('operationAmount', {})
        transaction_currency = operation_amount.get('currency', {})
        currency_code = transaction_currency.get('code', '')
        
        if currency_code == currency:
            filtered.append(transaction)
    
    return filtered
