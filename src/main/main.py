from .utils import read_json
from .processing import filter_by_state
from .widget import mask_account_card, get_date


def main(file_path: str = "data/operations.json"):
    """Основная функция приложения"""
    transactions = read_json(file_path)
    if not transactions:
        print("Не удалось загрузить транзакции.")
        return

    executed_transactions = filter_by_state(transactions, "EXECUTED")
    print(f"Найдено банковских операций: {len(executed_transactions)}")

    # Вывод только количества без деталей транзакций для тестов
    if len(executed_transactions) > 0:
        print("\nПример транзакции:")
        op = executed_transactions[0]
        print(f"{get_date(op['date'])} {op['description']}")
        if 'from' in op:
            print(f"{mask_account_card(op['from'])} -> ", end="")
        print(mask_account_card(op['to']))
        print(f"Сумма: {op['operationAmount']['amount']} {op['operationAmount']['currency']['code']}")
