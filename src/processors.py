import re
from collections import Counter
from typing import List, Dict, Any


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по заданной строке в описании с использованием регулярных выражений.

    Args:
        data: Список словарей с данными о банковских операциях
        search: Строка для поиска в описании операций

    Returns:
        Список словарей с операциями, у которых в описании есть искомая строка
    """
    if not data or not search:
        return []

    result = []
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    for transaction in data:
        description = transaction.get('description', '')
        if pattern.search(description):
            result.append(transaction)

    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество банковских операций по категориям.

    Args:
        data: Список словарей с данными о банковских операциях
        categories: Список категорий для подсчета

    Returns:
        Словарь с количеством операций по каждой категории
    """
    if not data:
        return {}

    # Приводим категории к нижнему регистру для case-insensitive сравнения
    categories_lower = [cat.lower() for cat in categories]

    # Собираем все описания
    descriptions = []
    for transaction in data:
        description = transaction.get('description', '').lower()
        if description:
            descriptions.append(description)

    # Фильтруем только нужные категории и подсчитываем
    filtered_descriptions = [desc for desc in descriptions if desc in categories_lower]
    counter = Counter(filtered_descriptions)

    # Восстанавливаем оригинальные названия категорий
    result = {}
    for category in categories:
        result[category] = counter.get(category.lower(), 0)

    return result