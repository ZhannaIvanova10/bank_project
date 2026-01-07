from unittest.mock import Mock, patch

import pytest

from src.api.currency_api import convert_to_rub, get_currency_rate


class TestExternalApi:
    @pytest.mark.parametrize(
        "currency, amount, expected",
        [
            ("USD", 100, 7500.0),
            ("EUR", 50, 4250.0),
            ("RUB", 200, 200.0),
        ],
    )
    def test_convert_to_rub(self, currency, amount, expected):
        """English docstring"""
        with patch("src.api.currency_api.get_currency_rate") as mock_rate:
            mock_rate.return_value = 75.0 if currency != "RUB" else 1.0
            assert convert_to_rub(currency, amount) == expected

    @patch("src.api.currency_api.requests.get")
    def test_get_currency_rate_success(self, mock_get):
        """English docstring"""
        mock_response = Mock()
        mock_response.json.return_value = {"rates": {"RUB": 75.0}}
        mock_get.return_value = mock_response

        with patch.dict("os.environ", {"EXCHANGE_RATE_API_KEY": "test"}):
            assert get_currency_rate("USD") == 75.0

    def test_get_currency_rate_rub(self):
        """English docstring"""
        assert get_currency_rate("RUB") == 1.0
