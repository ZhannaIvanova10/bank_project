from src.masks.masks import get_mask_card_number, get_mask_account


def mask_account_card(data: str) -> str | None:
    """
    Маскирует номер карты или счета в зависимости от типа данных.

    :param data: Строка с типом и номером карты/счета.
    :return: Замаскированная строка или None в случае ошибки.
    """
    parts = data.split()
    if len(parts) < 2:
        return None

    if parts[0].lower() == "счет":
        account_number = parts[-1]
        masked = get_mask_account(account_number)
        return f"{' '.join(parts[:-1])} {masked}"
    else:
        card_number = parts[-1]
        masked = get_mask_card_number(card_number)
        return f"{' '.join(parts[:-1])} {masked}"


def get_date(date_str: str) -> str | None:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    :param date_str: Строка с датой в формате ISO.
    :return: Дата в формате ДД.ММ.ГГГГ или None в случае ошибки.
    """
    from datetime import datetime
    try:
        date_obj = datetime.fromisoformat(date_str)
        return date_obj.strftime("%d.%m.%Y")
    except ValueError:
        return None
