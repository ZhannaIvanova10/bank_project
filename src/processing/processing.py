"""Модуль для обработки транзакций."""
from datetime import datetime
from typing import List, Dict, Any


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по статусу.
    
    Args:
        transactions: Список транзакций
        state: Статус для фильтрации (EXECUTED, CANCELED, PENDING)
    Returns:
        Отфильтрованный список транзакций
    """
    if not transactions:
        return []
    
    filtered = []
    for transaction in transactions:
        if transaction.get('state') == state:
            filtered.append(transaction)
    
    return filtered


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.
    Args:
        transactions: Список транзакций
        reverse: Если True - сортировка по убыванию (новые сначала), False - по возрастанию
        
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
    
    return sorted(transactions, key=get_date, reverse=reverse)
