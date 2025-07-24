from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета в зависимости от типа"""
    if "Счет" in account_info:
        parts = account_info.split()
        return f"{' '.join(parts[:-1])} {get_mask_account(parts[-1])}"
    else:
        parts = account_info.split()
        return f"{' '.join(parts[:-1])} {get_mask_card_number(parts[-1])}"


def get_date(date_str: str) -> str:
    """Преобразует дату из формата ISO в DD.MM.YYYY"""
    from datetime import datetime

    return datetime.fromisoformat(date_str).strftime("%d.%m.%Y")
