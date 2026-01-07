import re
from typing import List, Dict

def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Фильтрует список транзакций по строке поиска в описании.
    """
    result = []
    pattern = re.compile(search, re.IGNORECASE)
    for operation in data:
        description = operation.get("description", "")
        if pattern.search(description):
            result.append(operation)
    return result
