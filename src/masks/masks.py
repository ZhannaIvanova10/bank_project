import logging


def get_mask_card_number(card_number: str | int) -> str:
    """
    Маскирует номер карты в формате XXXX XX** **** XXXX.

    :param card_number: Номер карты в виде строки или числа.
    :return: Замаскированный номер карты.
    """
    card_str = str(card_number)
    if len(card_str) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр.")
    return f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"


def get_mask_account(account_number: str | int) -> str:
    """
    Маскирует номер счета в формате **XXXX.

    :param account_number: Номер счета в виде строки или числа.
    :return: Замаскированный номер счета.
    """
    account_str = str(account_number)
    if len(account_str) < 4:
        raise ValueError("Номер счета должен содержать не менее 4 цифр.")
    return f"**{account_str[-4:]}"
