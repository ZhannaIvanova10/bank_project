def filter_by_state(transactions: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует транзакции по статусу.

    :param transactions: Список транзакций.
    :param state: Статус для фильтрации (по умолчанию "EXECUTED").
    :return: Отфильтрованный список транзакций.
    """
    return [t for t in transactions if t.get("state", "").upper() == state.upper()]


def sort_by_date(transactions: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует транзакции по дате.

    :param transactions: Список транзакций.
    :param reverse: Флаг сортировки по убыванию (по умолчанию True).
    :return: Отсортированный список транзакций.
    """
    return sorted(transactions, key=lambda x: x.get("date", ""), reverse=reverse)
