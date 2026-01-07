from src.generators.generators import generate_transaction


def test_generate_transaction():
    transaction = generate_transaction()
    assert "amount" in transaction
    assert "date" in transaction
    assert isinstance(transaction["amount"], float)
