"""Модуль для работы с датами."""
from datetime import datetime


def format_date(date_str: str) -> str:
    """
    Форматирует дату из формата 'YYYY-MM-DDTHH:MM:SS' в 'DD.MM.YYYY'.
    
    Args:
        date_str: Строка с датой в формате 'YYYY-MM-DDTHH:MM:SS'
    
    Returns:
        Отформатированная дата в виде строки 'DD.MM.YYYY'
    """
    if not date_str:
        return ""
    try:
        # Пытаемся распарсить дату
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime("%d.%m.%Y")
    except (ValueError, AttributeError):
        # Если не удалось распарсить, возвращаем исходную строку
        return date_str
