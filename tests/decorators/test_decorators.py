"""Tests for decorators module."""

import os

from src.decorators.decorators import log


def test_log_to_file(tmp_path):
    """Test logging to file."""
    log_file = tmp_path / "test.log"

    @log(filename=log_file)
    def test_func(x):
        return x * 2

    test_func(2)
    assert os.path.exists(log_file)
    with open(log_file) as f:
        assert "test_func ok" in f.read()


def test_log_to_console(capsys):
    """Test logging to console."""

    @log()
    def test_func(x):
        return x * 2

    test_func(2)
    captured = capsys.readouterr()
    assert "test_func ok" in captured.out
