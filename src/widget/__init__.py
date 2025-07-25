from src.masks import get_mask_card_number, get_mask_account

def mask_account_card(data: str) -> str:
    """Обрабатывает как карты, так и счета"""
    if "Счет" in data:
        return f"Счет {get_mask_account(data.split()[-1])}"
    else:
        parts = data.split()
        return f"{' '.join(parts[:-1])} {get_mask_card_number(parts[-1])}"

def get_date(date_str: str) -> str:
    """Преобразует дату в формат ДД.ММ.ГГГГ"""
    date_part = date_str.split("T")[0]
    year, month, day = date_part.split("-")
    return f"{day}.{month}.{year}"
