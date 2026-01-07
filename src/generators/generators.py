from collections.abc import Iterator, Generator

def filter_by_currency(transactions: list[dict], currency: str) -> Iterator[dict]:
    """Фильтрует транзакции по валюте."""
    for transaction in transactions:
        op_amount = transaction.get("operationAmount", {})
        if op_amount.get("currency", {}).get("code") == currency:
            yield transaction

def transaction_descriptions(transactions: list[dict]) -> Generator[str, None, None]:
    """Генерирует описания транзакций."""
    for transaction in transactions:
        yield transaction.get("description", "")

def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """Генерирует номера карт."""
    for num in range(start, end + 1):
        yield f"{num:016d}"[:4] + " " + f"{num:016d}"[4:8] + " " + f"{num:016d}"[8:12] + " " + f"{num:016d}"[12:16]
