import pytest

from src.processing import filter_by_state, get_last_transactions, sort_by_date


class TestTransactionProcessing:
    @pytest.fixture
    def sample_transactions(self):
        return [
            {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
            {"id": 2, "state": "CANCELED", "date": "2023-01-02"},
            {"id": 3, "state": "EXECUTED", "date": "2023-01-03"},
            {"id": 4, "state": "PENDING", "date": "2023-01-04"},
        ]

    @pytest.mark.parametrize(
        "state, expected_ids",
        [
            ("EXECUTED", [1, 3]),
            ("CANCELED", [2]),
            ("PENDING", [4]),
            (None, [1, 3]),
        ],
    )
    def test_filter_by_state(self, sample_transactions, state, expected_ids):
        result = filter_by_state(sample_transactions, state)
        assert [t["id"] for t in result] == expected_ids

    def test_sort_by_date(self):
        transactions = [
            {"id": 1, "date": "2023-01-01"},
            {"id": 2, "date": "2023-01-03"},
            {"id": 3, "date": "2023-01-02"},
        ]
        assert [t["id"] for t in sort_by_date(transactions)] == [2, 3, 1]
        assert [t["id"] for t in sort_by_date(transactions, False)] == [1, 3, 2]

    @pytest.mark.parametrize(
        "count, expected_ids",
        [
            (2, [3, 1]),
            (3, [3, 1]),
            (10, [3, 1]),
        ],
    )
    def test_get_last_transactions(self, sample_transactions, count, expected_ids):
        result = get_last_transactions(sample_transactions, count)
        assert [t["id"] for t in result] == expected_ids
