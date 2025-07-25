# tests/conftest.py
import pytest

@pytest.fixture
def sample_transactions():
    return [
        {
            "date": "2024-01-01T00:00:00",
            "description": "Тестовая операция",
            "from": "Visa 1234567812345678",
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "RUB"}
            },
            "state": "EXECUTED"
        }
    ]
