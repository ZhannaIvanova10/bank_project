from src.processing import filter_by_state


def test_filter_by_state():
    transactions = [{"state": "EXECUTED"}, {"state": "CANCELED"}]
    filtered = filter_by_state(transactions, "EXECUTED")
    assert len(filtered) == 1
    assert filtered[0]["state"] == "EXECUTED"
