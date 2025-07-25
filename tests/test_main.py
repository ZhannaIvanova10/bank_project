from unittest.mock import patch
import pytest
from src.main import main

def test_main_empty_data(capsys):
    """Тест обработки пустых данных"""
    with patch('src.utils.read_json', return_value=[]):
        result = main("test_path.json")
        captured = capsys.readouterr()
        assert result == 0
        assert "Найдено банковских операций: 0" in captured.out

def test_main_no_executed(capsys):
    """Тест, когда нет выполненных операций"""
    test_data = [{
        "date": "2024-01-01T00:00:00",
        "state": "CANCELED",
        "description": "Тест",
        "operationAmount": {
            "amount": "100",
            "currency": {"code": "RUB"}
        },
        "from": "Visa 1234567890123456"
    }]
    with patch('src.utils.read_json', return_value=test_data):
        result = main("test_path.json")
        captured = capsys.readouterr()
        assert result == 0
        assert "Нет выполненных операций" in captured.out

def test_main_success(capsys):
    with patch('src.main.read_json') as mock_read:
        mock_read.return_value = [
            {
                "date": "2024-01-01T00:00:00",
                "description": "Test",
                "from": "Visa 1234567812345678",
                "operationAmount": {
                    "amount": "100",
                    "currency": {"code": "RUB"}
                },
                "state": "EXECUTED"
            }
        ]

        result = main()
        captured = capsys.readouterr()

        assert result == 0
        assert "Привет!" in captured.out
        assert "Test" in captured.out


def test_main_error(capsys):
    with patch('src.main.read_json') as mock_read:
        mock_read.side_effect = Exception("Test error")

        result = main()
        captured = capsys.readouterr()

        assert result == 1
        assert "Ошибка: Test error" in captured.err

def test_main_with_data(capsys, sample_transactions):
    """Тест с реальными данными"""
    with patch('src.utils.read_json', return_value=sample_transactions):
        result = main()
        captured = capsys.readouterr()
        assert result == 0
        assert "Найдено банковских операций: 1" in captured.out
        assert "Тестовая операция" in captured.out
