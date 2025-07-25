import pytest
from src.utils import read_json
import os
import json

@pytest.fixture
def create_test_json(tmp_path):
    test_data = [{"test": "data"}]
    file_path = tmp_path / "test.json"
    with open(file_path, 'w') as f:
        json.dump(test_data, f)
    return file_path

def test_read_json_valid(create_test_json):
    data = read_json(create_test_json)
    assert isinstance(data, list)
    assert len(data) == 1

def test_read_json_invalid(tmp_path):
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("{invalid json}")
    assert read_json(invalid_file) == []

def test_read_json_not_found():
    assert read_json("nonexistent.json") == []
