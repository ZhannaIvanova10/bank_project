import pytest

from utils.processors import process_bank_operations, process_bank_search


class TestProcessors:
    """Тесты для процессоров данных."""

    @pytest.fixture
    def sample_data(self):
        return [
            {"description": "Перевод организации", "state": "EXECUTED"},
            {"description": "Открытие вклада", "state": "EXECUTED"},
            {"description": "Перевод с карты на карту", "state": "CANCELED"},
            {"description": "Оплата услуг", "state": "PENDING"},
        ]

    def test_process_bank_search_found(self, sample_data):
        """Тест поиска транзакций - найдены совпадения."""
        result = process_bank_search(sample_data, "перевод")
        assert len(result) == 2
        assert all("перевод" in transaction["description"].lower() for transaction in result)

    def test_process_bank_search_not_found(self, sample_data):
        """Тест поиска транзакций - совпадений нет."""
        result = process_bank_search(sample_data, "несуществующее")
        assert len(result) == 0

    def test_process_bank_search_case_insensitive(self, sample_data):
        """Тест case-insensitive поиска."""
        result = process_bank_search(sample_data, "ПЕРЕВОД")
        assert len(result) == 2

    def test_process_bank_search_empty_data(self):
        """Тест поиска с пустыми данными."""
        result = process_bank_search([], "перевод")
        assert result == []

    def test_process_bank_operations(self, sample_data):
        """Тест подсчета операций по категориям."""
        categories = ["Перевод организации", "Открытие вклада", "Несуществующая"]
        result = process_bank_operations(sample_data, categories)

        assert result["Перевод организации"] == 1
        assert result["Открытие вклада"] == 1
        assert result["Несуществующая"] == 0

    def test_process_bank_operations_case_insensitive(self, sample_data):
        """Тест case-insensitive подсчета операций."""
        categories = ["ПЕРЕВОД ОРГАНИЗАЦИИ", "открытие вклада"]
        result = process_bank_operations(sample_data, categories)

        assert result["ПЕРЕВОД ОРГАНИЗАЦИИ"] == 1
        assert result["открытие вклада"] == 1

    def test_process_bank_operations_empty_data(self):
        """Тест подсчета операций с пустыми данными."""
        result = process_bank_operations([], ["категория"])
        assert result == {}
