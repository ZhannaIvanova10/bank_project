import pytest
from src.generators import card_number_generator, transaction_descriptions


def test_card_number_generator():
    gen = card_number_generator(1, 3)
    assert next(gen) == "0000 0000 0000 0001"
    assert next(gen) == "0000 0000 0000 0002"
    assert next(gen) == "0000 0000 0000 0003"


def test_transaction_descriptions():
    transactions = [{"description": "test1"}, {"description": "test2"}]
    gen = transaction_descriptions(transactions)
    assert next(gen) == "test1"
    assert next(gen) == "test2"
