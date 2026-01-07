import re
from datetime import datetime, timedelta
from typing import Optional

import pytest

from src.widget import format_date as get_date
from src.widget import mask_account_card


class TestWidgetFunctions:
    # Тесты для mask_account_card
    @pytest.mark.parametrize(
        "input_str, expected",
        [
            # Стандартные случаи карт
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
            ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
            ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
            ("МИР 1234123412341234", "МИР 1234 12** **** 1234"),
            ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
            # Стандартные случаи счетов
            ("Счет 73654108430135874305", "Счет **4305"),
            ("Счет 1234567890123456", "Счет **3456"),
            ("Account 9876543210123456", "Account **3456"),
            # Крайние случаи и ошибки
            ("", None),
            (None, None),
            ("Счет без номера", "Счет без номера"),
            ("Карта 1234", "Карта 1234"),
            ("Just text", "Just text"),
            # Специальные символы
            ("Visa-1234567890123456", "Visa-1234 56** **** 3456"),
            ("Счёт 1234567890123456", "Счёт **3456"),  # С "ё"
        ],
        ids=[
            "Visa Platinum",
            "Maestro",
            "MasterCard",
            "МИР",
            "Visa Classic",
            "Счет 20 цифр",
            "Счет 16 цифр",
            "Account на английском",
            "Пустая строка",
            "None",
            "Счет без номера",
            "Короткий номер карты",
            "Просто текст",
            "С дефисом",
            "С буквой ё",
        ],
    )
    def test_mask_account_card(self, input_str: Optional[str], expected: Optional[str]) -> None:
        """English docstring"""
        assert mask_account_card(input_str) == expected

    # Тесты для get_date
    @pytest.mark.parametrize(
        "date_str, expected",
        [
            ("2024-03-11T02:26:18.671407", "11.03.2024"),
            ("2020-12-31T23:59:59.999999", "31.12.2020"),
            ("1999-01-01T00:00:00.000000", "01.01.1999"),
            # Неполные форматы дат
            ("2024-03-11", "11.03.2024"),
            ("2024-03-11T02:26:18", "11.03.2024"),
            # Некорректные данные
            ("не дата", "не дата"),
            ("", ""),
            ("2024-13-11", "2024-13-11"),  # Несуществующая дата
        ],
        ids=[
            "Стандартная дата",
            "Конец года",
            "Начало года",
            "Только дата",
            "Без миллисекунд",
            "Текст",
            "Пустая строка",
            "Несуществующая дата",
        ],
    )
    def test_get_date(self, date_str: str, expected: str) -> None:
        """English docstring"""
        assert get_date(date_str) == expected

    def test_get_date_current_time(self) -> None:
        """English docstring"""
        now_iso = datetime.now().isoformat()
        result = get_date(now_iso)
        assert re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", result)

    def test_get_date_future_date(self) -> None:
        """English docstring"""
        future_date = (datetime.now() + timedelta(days=365)).isoformat()
        result = get_date(future_date)
        assert re.fullmatch(r"\d{2}\.\d{2}\.\d{4}", result)

    def test_get_date_invalid_type(self) -> None:
        """English docstring"""
        with pytest.raises(ValueError):
            get_date(12345)  # type: ignore
