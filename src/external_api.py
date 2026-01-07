import os
import requests
from dotenv import load_dotenv

load_dotenv()


def convert_to_rub(transaction: dict) -> float | None:
    """
    Конвертирует сумму транзакции в рубли.

    :param transaction: Словарь с данными транзакции.
    :return: Сумма в рублях или None в случае ошибки.
    """
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency = transaction["operationAmount"]["currency"]["code"]

        if currency == "RUB":
            return amount

        api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        if not api_key:
            raise ValueError("API ключ не найден.")

        url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}&symbols=RUB"
        headers = {"apikey": api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        rate = response.json()["rates"]["RUB"]
        return amount * rate
    except (KeyError, ValueError, requests.RequestException):
        return None
