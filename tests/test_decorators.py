import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent))

from src.decorators.decorators import log


class TestLogDecorator:
    def test_log_without_file(self, capsys):
        """English docstring"""

        @log()
        def test_func():
            return "success"

        result = test_func()
        captured = capsys.readouterr()
        assert result == "success"
        assert "test_func - успешно" not in captured.out

    def test_log_with_file(self, tmp_path):
        """English docstring"""
        log_file = tmp_path / "test_log.txt"

        @log(filename=str(log_file))
        def test_func():
            return "success"

        test_func()
        # Чтение файла с указанием кодировки UTF-8
        content = log_file.read_text(encoding="utf-8")
        assert "test_func - успешно" in content

    def test_log_with_exception(self, tmp_path):
        """English docstring"""
        error_log = tmp_path / "error_log.txt"

        @log(filename=str(error_log))
        def faulty_func():
            raise ValueError("Test error")

        with pytest.raises(ValueError, match="Test error"):
            faulty_func()

        # Чтение файла с указанием кодировки UTF-8
        content = error_log.read_text(encoding="utf-8")
        assert "faulty_func - ошибка: Test error" in content
