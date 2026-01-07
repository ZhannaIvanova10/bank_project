import json
import csv
import openpyxl
from typing import List, Dict, Any


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу

    Returns:
        Список словарей с данными о транзакциях
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка при чтении JSON-файла: {e}")
        return []


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные из CSV-файла.

    Args:
        file_path: Путь к CSV-файлу

    Returns:
        Список словарей с данными о транзакциях
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except (FileNotFoundError, csv.Error) as e:
        print(f"Ошибка при чтении CSV-файла: {e}")
        return []


def read_xlsx_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные из XLSX-файла.

    Args:
        file_path: Путь к XLSX-файлу

    Returns:
        Список словарей с данными о транзакциях
    """
    try:
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        headers = [cell.value for cell in sheet[1]]
        data = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            transaction = dict(zip(headers, row))
            data.append(transaction)

        return data
    except (FileNotFoundError, openpyxl.utils.exceptions.InvalidFileException) as e:
        print(f"Ошибка при чтении XLSX-файла: {e}")
        return []