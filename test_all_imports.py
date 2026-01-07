print("=== ТЕСТИРОВАНИЕ ВСЕХ ИМПОРТОВ ===")

modules_to_test = [
    ("src.masks.masks", ["get_mask_card_number", "get_mask_account"]),
    ("src.utils.date_utils", ["format_date"]),
    ("src.utils.utils", ["read_json_file", "validate_date_format", "get_last_five_executed"]),
    ("src.utils.file_handlers", ["read_json_file", "read_csv_file", "read_xlsx_file"]),
    ("src.utils.filters", ["filter_by_status", "filter_by_currency", "sort_by_date"]),
    ("src.processing.processing", ["filter_by_state", "sort_by_date"]),
    ("src.search", ["process_bank_search"]),
    ("src.counter", ["process_bank_operations"]),
]

all_ok = True

for module_path, functions in modules_to_test:
    print(f"\n--- {module_path} ---")
    try:
        # Динамический импорт
        import importlib
        module = importlib.import_module(module_path)
        
        for func in functions:
            if hasattr(module, func):
                print(f"  ✅ {func}")
            else:
                print(f"  ❌ {func} - не найден")
                all_ok = False
    except ImportError as e:
        print(f"  ❌ Ошибка импорта: {e}")
        all_ok = False
    except Exception as e:
        print(f"  ❌ Неожиданная ошибка: {e}")
        all_ok = False

print(f"\n{'='*50}")
if all_ok:
    print("🎉 ВСЕ ИМПОРТЫ РАБОТАЮТ КОРРЕКТНО!")
else:
    print("⚠ ЕСТЬ ПРОБЛЕМЫ С ИМПОРТАМИ!")
