"""Модуль для чтения файлов разных форматов."""
import json
import csv
from datetime import datetime
from typing import List, Dict, Any
import openpyxl


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные из JSON файла.
    
    Args:
        file_path: Путь к JSON файлу
        
    Returns:
        Список словарей с данными о транзакциях
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка чтения JSON файла {file_path}: {e}")
        return []


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные из CSV файла.
    
    Args:
        file_path: Путь к CSV файлу
        
    Returns:
        Список словарей с данными о транзакциях
    """
    transactions = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(row)
        return transactions
    except (FileNotFoundError, csv.Error) as e:
        print(f"Ошибка чтения CSV файла {file_path}: {e}")
        return []
def read_xlsx_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает данные из XLSX файла.
    
    Args:
        file_path: Путь к XLSX файлу
        
    Returns:
        Список словарей с данными о транзакциях
    """
    transactions = []
    try:
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        sheet = workbook.active
        # Получаем заголовки из первой строки
        headers = []
        for cell in sheet[1]:
            if cell.value is not None:
                headers.append(str(cell.value))
        
        if not headers:
            print(f"⚠ В файле {file_path} нет заголовков в первой строке")
            return []
        
        # Читаем данные
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Пропускаем пустые строки
            if all(cell is None for cell in row):
                continue
                
            transaction = {}
            for i, value in enumerate(row):
                if i < len(headers) and value is not None:
                    transaction[headers[i]] = value
            
            if transaction:  # Добавляем только если есть данные
                transactions.append(transaction)
        return transactions
    
    except Exception as e:
        print(f"❌ Ошибка чтения XLSX файла {file_path}: {e}")
        return []
