import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Union

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class BankLogger:
    """Logger configuration for banking application."""

    def __init__(self):
        self._configured = False

    def setup(
        self,
        log_level: Union[int, str] = logging.INFO,
        log_file: Optional[Union[str, Path]] = None,
        file_log_level: Union[int, str] = logging.DEBUG,
        console_log_level: Union[int, str] = logging.INFO,
        rotation: str = "1 MB",
    ) -> None:
        """Initialize logging configuration."""
        if self._configured:
            return

        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True, mode=0o755)
        log_file = Path(log_file) if log_file else logs_dir / "app.log"

        logger = logging.getLogger()
        logger.setLevel(log_level)

        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

        try:
            file_handler = RotatingFileHandler(
                log_file, maxBytes=self._parse_rotation(rotation), backupCount=5, encoding="utf-8"
            )
            file_handler.setLevel(file_log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except IOError:
            sys.stderr.write("Failed to create log file\n")

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(console_log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        self._configure_third_party_loggers()
        self._configured = True

    def _parse_rotation(self, rotation: str) -> int:
        """Convert rotation string to bytes."""
        units = {"KB": 1024, "MB": 1024**2, "GB": 1024**3}
        if " " in rotation:
            size, unit = rotation.split()
            return int(size) * units.get(unit.upper(), 1)
        return int(rotation) if rotation.isdigit() else 1024**2

    def _configure_third_party_loggers(self) -> None:
        """Configure logging for third-party libraries."""
        for lib in ["requests", "urllib3", "pandas", "openpyxl"]:
            logging.getLogger(lib).setLevel(logging.WARNING)

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """Get configured logger instance."""
        if not self._configured:
            self.setup()
        return logging.getLogger(name)


bank_logger = BankLogger()
get_logger = bank_logger.get_logger
