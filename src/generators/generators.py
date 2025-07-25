from typing import Iterator, List, Dict, Any
from collections import Counter


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по валюте

    :param transactions: Список транзакций
    :param currency: Код валюты (например "USD")
    :return: Итератор по подходящим транзакциям
    """
    for transaction in transactions:
        op_amount = transaction.get("operationAmount", {})
        if op_amount.get("currency", {}).get("code") == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генерирует описания транзакций

    :param transactions: Список транзакций
    :return: Итератор по описаниям
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера карт в диапазоне

    :param start: Начальный номер
    :param end: Конечный номер
    :return: Итератор по номерам карт в формате "XXXX XXXX XXXX XXXX"
    """
    for num in range(start, end + 1):
        yield f"{num:016d}"[:4] + " " + f"{num:016d}"[4:8] + " " + \
            f"{num:016d}"[8:12] + " " + f"{num:016d}"[12:16]
