from datetime import datetime
from .masks import get_mask_card_number, get_mask_account


def mask_account_card(account_info: str) -> str:
    """
    Маскирует карту/счет в зависимости от типа

    :param account_info: Строка типа "Visa Platinum 7000792289606361" или "Счет 73654108430135874305"
    :return: Замаскированная строка
    """
    parts = account_info.split()
    if len(parts) < 2:
        return account_info

    *card_type, number = parts
    card_type = ' '.join(card_type)

    if card_type.lower() == 'счет':
        return f"{card_type} {get_mask_account(number)}"
    return f"{card_type} {get_mask_card_number(number)}"


def get_date(date_str: str) -> str:
    """
    Форматирует дату из ISO в DD.MM.YYYY

    :param date_str: Дата в формате "2019-08-26T10:50:58.294041"
    :return: Дата в формате "26.08.2019"
    """
    try:
        date_obj = datetime.fromisoformat(date_str)
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        return date_str
