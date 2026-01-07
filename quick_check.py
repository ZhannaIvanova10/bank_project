#!/usr/bin/env python3
import os

print("🔍 БЫСТРАЯ ПРОВЕРКА ФАЙЛОВ ДЗ 13.2")
print("=" * 40)
files = {
    "src/search.py": "Функция поиска (process_bank_search)",
    "src/counter.py": "Функция подсчета (process_bank_operations)",
    "main.py": "Основная программа",
    "data/operations.json": "Тестовые данные",
    "test_homework.py": "Тестовый скрипт",
}

all_ok = True
for file_path, description in files.items():
    if os.path.exists(file_path):
        print(f"✅ {description}")
        print(f"   📍 {file_path}")
        # Простая проверка содержимого
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                size = len(content)
                print(f"   📏 Размер: {size} символов")

                if "search.py" in file_path:
                    if "process_bank_search" in content and "import re" in content:
                        print("   ✓ Содержит process_bank_search и re")
                elif "counter.py" in file_path:
                    if "process_bank_operations" in content and "Counter" in content:
                        print("   ✓ Содержит process_bank_operations и Counter")
        except:
            print("   ⚠ Не удалось прочитать файл")
    else:
        print(f"❌ {description}")
        print(f"   📍 {file_path} - ОТСУТСТВУЕТ!")
        all_ok = False
    print()
print("=" * 40)
if all_ok:
    print("🎉 ВСЕ ФАЙЛЫ НА МЕСТЕ! ПРОЕКТ ГОТОВ!")
    print("\n🚀 Создайте Pull Request по ссылке:")
    print("https://github.com/ZhannaIvanova10/bank_project/compare/develop...feature/final-integration")
else:
    print("⚠ НЕКОТОРЫЕ ФАЙЛЫ ОТСУТСТВУЮТ!")
