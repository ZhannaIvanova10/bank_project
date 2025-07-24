import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging():
    """Настройка логирования для всего проекта"""
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Настройка root логгера
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Файловый обработчик
    file_handler = RotatingFileHandler("logs/bank_project.log", maxBytes=1024 * 1024, backupCount=5)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)


if __name__ == "__main__":
    setup_logging()
    # Дальнейшая логика приложения
