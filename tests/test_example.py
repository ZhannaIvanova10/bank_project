import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent))

import re
from datetime import datetime

import pytest

from widget import format_date as get_date
from widget import mask_account_card


class TestWidgetFunctions:
    @pytest.mark.parametrize(
        "card, expected",
        [
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
            ("Счет 73654108430135874305", "Счет **4305"),
            ("MasterCard 1234123412341234", "MasterCard 1234 12** **** 1234"),
            ("", ""),
            ("Счет", "Счет"),
        ],
    )
    def test_mask_account_card(self, card, expected):
        """English docstring"""
        assert mask_account_card(card) == expected

    def test_get_date_current_time(self):
        """English docstring"""
        now = datetime.now().isoformat()
        result = get_date(now)
        assert re.match(r"\d{2}\.\d{2}\.\d{4}", result)
