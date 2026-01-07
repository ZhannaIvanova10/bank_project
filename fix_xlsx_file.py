import json
import openpyxl
from openpyxl import Workbook

print("=== Исправление XLSX файла ===")

# 1. Проверим что в файле
try:
    with open('data/transactions.xlsx', 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"Размер файла: {len(content)} байт")
        print(f"Первые 200 символов: {content[:200]}")
        
        # Пробуем прочитать как JSON
        try:
            data = json.loads(content)
            print(f"✅ Файл содержит JSON данные: {len(data)} записей")
            # Создаем настоящий XLSX
            wb = Workbook()
            ws = wb.active
            ws.title = "Transactions"
            
            # Добавляем заголовки из первого элемента
            if data and isinstance(data, list) and len(data) > 0:
                headers = list(data[0].keys())
                ws.append(headers)
                
                # Добавляем данные
                for item in data[:100]:  # Ограничим 100 записями для теста
                    row = [item.get(key, '') for key in headers]
                    ws.append(row)
                
                wb.save('data/transactions_real.xlsx')
                print(f"✅ Создан настоящий XLSX файл: data/transactions_real.xlsx")
                print(f"✅ Добавлено {min(len(data), 100)} записей")
            else:
                print("❌ Нет данных в JSON")
        except json.JSONDecodeError as e:
            print(f"❌ Не удалось распарсить как JSON: {e}")
            
except Exception as e:
    print(f"❌ Ошибка чтения файла: {e}")

# 2. Создаем простой тестовый XLSX
print("\n=== Создаем простой тестовый XLSX ===")
try:
    wb = Workbook()
    ws = wb.active
    ws.title = "Bank Transactions"
    
    # Заголовки
    headers = ["id", "state", "date", "amount", "currency", "description", "from", "to"]
    ws.append(headers)
    # Тестовые данные (5 записей)
    test_data = [
        [1, "EXECUTED", "2023-12-01T10:30:00", 15000.50, "RUB", "Перевод организации", "Счет 1234567890123456", "Счет 6543210987654321"],
        [2, "EXECUTED", "2023-11-15T14:20:00", 50000.00, "RUB", "Открытие вклада", "", "Счет 8888888888888888"],
        [3, "EXECUTED", "2023-10-25T09:15:00", 2500.75, "RUB", "Оплата услуг", "Счет 4444444444444444", "Счет 1111111111111111"],
        [4, "CANCELED", "2023-09-10T16:45:00", 10000.00, "USD", "Покупка валюты", "Счет 5555555555555555", "Карта 1234567812345678"],
        [5, "PENDING", "2023-08-05T11:10:00", 7500.25, "EUR", "Международный перевод", "Карта 8765432187654321", "Счет 9999999999999999"]
    ]
    for row in test_data:
        ws.append(row)
    
    wb.save('data/test_transactions.xlsx')
    print("✅ Создан test_transactions.xlsx с 5 тестовыми записями")
    
except Exception as e:
    print(f"❌ Ошибка создания XLSX: {e}")
