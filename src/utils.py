# src/utils.py
import json
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


def read_json_file(file_path: str) -> List[Dict]:
    """Читает JSON файл с транзакциями"""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                logger.error(f"File {file_path} does not contain a list")
                return []
            return data
    except FileNotFoundError:
        logger.error(f"File {file_path} not found")
        return []
    except json.JSONDecodeError:
        logger.error(f"File {file_path} is not valid JSON")
        return []
