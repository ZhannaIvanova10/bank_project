import pytest
from src.processing import filter_by_state, sort_by_date

@pytest.fixture
def sample_transactions():
    return [
        {"date": "2024-01-01", "state": "EXECUTED"},
        {"date": "2024-01-02", "state": "CANCELED"},
        {"date": "2024-01-03", "state": "EXECUTED"}
    ]

def test_filter_by_state(sample_transactions):
    filtered = filter_by_state(sample_transactions)
    assert len(filtered) == 2
    assert all(t["state"] == "EXECUTED" for t in filtered)

def test_sort_by_date(sample_transactions):
    sorted_trans = sort_by_date(sample_transactions)
    assert sorted_trans[0]["date"] == "2024-01-03"
    assert sorted_trans[-1]["date"] == "2024-01-01"
