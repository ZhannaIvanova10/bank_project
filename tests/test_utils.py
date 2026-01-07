from datetime import datetime

import pytest

from src.utils import get_last_five_executed, read_json_file, validate_date_format


@pytest.fixture
def sample_transactions():
    return [
        {"state": "EXECUTED", "date": "2023-01-01"},
        {"state": "PENDING", "date": "2023-01-02"},
        {"state": "EXECUTED", "date": "2023-01-03"},
        {"state": "EXECUTED", "date": "2023-01-04"},
        {"state": "CANCELLED", "date": "2023-01-05"},
        {"state": "EXECUTED", "date": "2023-01-06"},
    ]


def test_get_last_five_executed(sample_transactions):
    result = get_last_five_executed(sample_transactions)
    assert len(result) == 4  # Only EXECUTED
    assert result[0]["date"] == "2023-01-06"


def test_validate_date_format():
    assert validate_date_format("2023-01-01") is True
    assert validate_date_format("01-01-2023") is False
