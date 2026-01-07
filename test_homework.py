#!/usr/bin/env python3
"""
Отдельный тестовый файл для проверки домашнего задания.
Не зависит от структуры проекта.
"""
import sys
import os
import re
from collections import Counter
from typing import List, Dict

# Добавляем текущую директорию в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("ТЕСТИРОВАНИЕ ДОМАШНЕГО ЗАДАНИЯ 13.2")
print("=" * 60)

# Тест 1: Проверка search.py
print("\n1. ТЕСТИРОВАНИЕ ФУНКЦИИ ПОИСКА (search.py)")
print("-" * 40)

try:
    # Если файл существует, импортируем его
    if os.path.exists("src/search.py"):
        # Читаем файл как модуль
        import importlib.util
        spec = importlib.util.spec_from_file_location("search_module", "src/search.py")
        search_module = importlib.util.module_from_spec(spec)
        
        # Исполняем код модуля
        with open("src/search.py", "r", encoding="utf-8") as f:
            code = f.read()
            exec(code, search_module.__dict__)
        
        # Получаем функцию
        process_bank_search = search_module.process_bank_search

        # Тестовые данные
        test_data = [
            {"id": 1, "description": "Перевод организации", "amount": 100},
            {"id": 2, "description": "Открытие вклада", "amount": 200},
            {"id": 3, "description": "Перевод с карты", "amount": 300},
        ]
        
        # Тест
        result = process_bank_search(test_data, "Перевод")
        
        if len(result) == 2:
            print("✅ process_bank_search работает корректно!")
            print(f"   Найдено {len(result)} операций с 'Перевод'")
            print(f"   ID найденных операций: {[op['id'] for op in result]}")
        else:
            print(f"❌ Ошибка: ожидалось 2 операции, получено {len(result)}")
    else:
        print("❌ Файл src/search.py не найден")
        
except Exception as e:
    print(f"❌ Ошибка тестирования search: {e}")

# Тест 2: Проверка counter.py
print("\n2. ТЕСТИРОВАНИЕ ФУНКЦИИ ПОДСЧЕТА (counter.py)")
print("-" * 40)

try:
    if os.path.exists("src/counter.py"):
        import importlib.util
        spec = importlib.util.spec_from_file_location("counter_module", "src/counter.py")
        counter_module = importlib.util.module_from_spec(spec)
        
        with open("src/counter.py", "r", encoding="utf-8") as f:
            code = f.read()
            exec(code, counter_module.__dict__)
        
        process_bank_operations = counter_module.process_bank_operations
        # Тестовые данные
        test_data = [
            {"description": "Перевод", "amount": 100},
            {"description": "Перевод", "amount": 200},
            {"description": "Вклад", "amount": 300},
            {"description": "Платеж", "amount": 400},
        ]
        
        # Тест
        categories = ["Перевод", "Вклад", "Платеж", "Кредит"]
        result = process_bank_operations(test_data, categories)
        
        expected = {"Перевод": 2, "Вклад": 1, "Платеж": 1, "Кредит": 0}
        
        if result == expected:
            print("✅ process_bank_operations работает корректно!")
            print(f"   Результат: {result}")
        else:
            print(f"❌ Ошибка: ожидалось {expected}, получено {result}")
    else:
        print("❌ Файл src/counter.py не найден")
        
except Exception as e:
    print(f"❌ Ошибка тестирования counter: {e}")

# Тест 3: Проверка файла данных
print("\n3. ПРОВЕРКА ФАЙЛА ДАННЫХ")
print("-" * 40)

if os.path.exists("data/operations.json"):
    try:
        import json
        with open("data/operations.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        print(f"✅ Файл data/operations.json существует и корректный")
        print(f"   Загружено {len(data)} операций")
        # Проверяем структуру данных
        if len(data) > 0:
            sample = data[0]
            print(f"   Пример операции:")
            print(f"     Описание: {sample.get('description', 'Нет')}")
            print(f"     Сумма: {sample.get('amount', sample.get('operationAmount', {}).get('amount', 'Нет'))}")
            print(f"     Статус: {sample.get('state', 'Нет')}")
            
    except Exception as e:
        print(f"❌ Ошибка чтения файла: {e}")
else:
    print("❌ Файл data/operations.json не найден")

# Тест 4: Проверка основной программы
print("\n4. ПРОВЕРКА ОСНОВНОЙ ПРОГРАММЫ")
print("-" * 40)

if os.path.exists("main_simple.py"):
    print("✅ Файл main_simple.py существует")
    
    # Проверяем что файл содержит основные функции
    with open("main_simple.py", "r", encoding="utf-8") as f:
        content = f.read()
        
    required_functions = [
        "def process_bank_search",
        "def process_bank_operations", 
        "def main()"
    ]
    
    all_found = True
    for func in required_functions:
        if func in content:
            print(f"   ✅ Найдена {func}")
        else:
            print(f"   ❌ Не найдена {func}")
            all_found = False
    if all_found:
        print("✅ Основная программа содержит все необходимые функции")
    else:
        print("⚠ Основной программе не хватает некоторых функций")
        
else:
    print("❌ Файл main_simple.py не найден")

# Итоги
print("\n" + "=" * 60)
print("ИТОГИ ПРОВЕРКИ")
print("=" * 60)

# Проверяем наличие всех необходимых файлов
required_files = [
    ("src/search.py", "Функция поиска"),
    ("src/counter.py", "Функция подсчета"),
    ("main_simple.py", "Основная программа"),
    ("data/operations.json", "Тестовые данные"),
]

all_files_exist = True
for filepath, description in required_files:
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
    else:
        print(f"❌ {description}: {filepath} - НЕ НАЙДЕН")
        all_files_exist = False

if all_files_exist:
    print("\n🎉 ВСЕ НЕОБХОДИМЫЕ ФАЙЛЫ СОЗДАНЫ!")
    print("📋 Проект готов к сдаче.")
    print("\nСледующие шаги:")
    print("1. git push origin feature/final-integration")
    print("2. Создать Pull Request на GitHub")
    print("3. Прикрепить ссылку на PR как ответ на задание")
else:
    print("\n⚠ НЕКОТОРЫЕ ФАЙЛЫ ОТСУТСТВУЮТ")
    print("Создайте недостающие файлы перед сдачей.")

print("\n" + "=" * 60)
