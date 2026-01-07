import pytest
from utils.filters import filter_by_status, sort_by_date, filter_by_currency


class TestFilters:
    """Тесты для фильтров данных."""

    @pytest.fixture
    def sample_data(self):
        return [
            {'date': '2023-01-01T12:00:00Z', 'state': 'EXECUTED',
             'operationAmount': {'currency': {'code': 'RUB'}}},
            {'date': '2023-01-02T12:00:00Z', 'state': 'CANCELED',
             'operationAmount': {'currency': {'code': 'USD'}}},
            {'date': '2023-01-03T12:00:00Z', 'state': 'EXECUTED',
             'operationAmount': {'currency': {'code': 'EUR'}}}
        ]

    def test_filter_by_status_found(self, sample_data):
        """Тест фильтрации по статусу - найдены совпадения."""
        result = filter_by_status(sample_data, 'executed')
        assert len(result) == 2
        assert all(transaction['state'].lower() == 'executed' for transaction in result)

    def test_filter_by_status_not_found(self, sample_data):
        """Тест фильтрации по статусу - совпадений нет."""
        result = filter_by_status(sample_data, 'pending')
        assert len(result) == 0

    def test_filter_by_status_case_insensitive(self, sample_data):
        """Тест case-insensitive фильтрации по статусу."""
        result = filter_by_status(sample_data, 'EXECUTED')
        assert len(result) == 2

    def test_sort_by_date_ascending(self, sample_data):
        """Тест сортировки по дате по возрастанию."""
        result = sort_by_date(sample_data, reverse=False)
        dates = [transaction['date'] for transaction in result]
        assert dates == sorted(dates)

    def test_sort_by_date_descending(self, sample_data):
        """Тест сортировки по дате по убыванию."""
        result = sort_by_date(sample_data, reverse=True)
        dates = [transaction['date'] for transaction in result]
        assert dates == sorted(dates, reverse=True)

    def test_filter_by_currency(self, sample_data):
        """Тест фильтрации по валюте."""
        result = filter_by_currency(sample_data, 'RUB')
        assert len(result) == 1
        assert result[0]['operationAmount']['currency']['code'] == 'RUB'

    def test_filter_by_currency_case_insensitive(self, sample_data):
        """Тест case-insensitive фильтрации по валюте."""
        result = filter_by_currency(sample_data, 'rub')
        assert len(result) == 1