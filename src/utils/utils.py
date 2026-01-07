"""Утилиты для работы с банковскими транзакциями."""
import json
from datetime import datetime
from typing import List, Dict, Any
def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные из JSON файла.
    
    Args:
        file_path: Путь к JSON файлу
        
    Returns:
        Список словарей с данными о транзакциях
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка чтения JSON файла {file_path}: {e}")
        return []
def validate_date_format(date_str: str, date_format: str = "%Y-%m-%d") -> bool:
    """
    Проверяет, соответствует ли строка заданному формату даты.
    
    Args:
        date_str: Строка с датой
        date_format: Формат даты для проверки
        
    Returns:
        True если строка соответствует формату, иначе False
    """
    try:
        datetime.strptime(date_str, date_format)
        return True
    except (ValueError, TypeError):
        return False
def get_last_five_executed(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Возвращает последние 5 выполненных операций.
    
    Args:
        transactions: Список транзакций
        
    Returns:
        Последние 5 выполненных операций, отсортированных по дате (от новых к старым)
    """
    # Фильтруем выполненные операции
    executed = [t for t in transactions if t.get('state') == 'EXECUTED']
    
    # Сортируем по дате (от новых к старым)
    def get_date(transaction):
        date_str = transaction.get('date', '')
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return datetime.min
    
    sorted_transactions = sorted(executed, key=get_date, reverse=True)
    # Возвращаем первые 5 или все, если меньше
    return sorted_transactions[:5]
