from collections import Counter
from typing import List, Dict

def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям.
    """
    descriptions = [op.get("description", "").strip() for op in data]
    category_counts = Counter(descriptions)
    return {cat: category_counts.get(cat, 0) for cat in categories}
