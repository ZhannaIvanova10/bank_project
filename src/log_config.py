import logging
from pathlib import Path
from typing import Dict, Optional


def setup_logging(
    log_dir: str = "logs",
    console_level: Optional[str] = "INFO",
    file_levels: Optional[Dict[str, str]] = None,
) -> None:
    """English docstring"""
    try:
        logs_dir = Path(log_dir)
        logs_dir.mkdir(exist_ok=True, mode=0o755)

        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)

        # Консольный обработчик
        if console_level:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, console_level))
            console_handler.setFormatter(formatter)
            logging.getLogger().addHandler(console_handler)

        # Файловые обработчики
        file_levels = file_levels or {"utils": "DEBUG", "masks": "DEBUG"}

        for module, level in file_levels.items():
            logger = logging.getLogger(f"src.{module}")
            logger.setLevel(getattr(logging, level))
            file_handler = logging.FileHandler(
                logs_dir / f"{module}.log", mode="a", encoding="utf-8"  # Теперь дозапись
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    except Exception as e:
        logging.error(f"Ошибка настройки логирования: {e}")
        raise
