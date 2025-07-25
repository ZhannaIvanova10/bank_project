from typing import List, Dict


def filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Фильтрует транзакции по статусу

    :param transactions: Список транзакций
    :param state: Статус для фильтрации (по умолчанию "EXECUTED")
    :return: Отфильтрованный список транзакций
    """
    return [t for t in transactions if t.get("state") == state]


def sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Сортирует транзакции по дате

    :param transactions: Список транзакций
    :param reverse: Сортировка по убыванию (по умолчанию True)
    :return: Отсортированный список транзакций
    """
    return sorted(transactions, key=lambda x: x["date"], reverse=reverse)
