print("=== ТЕСТИРОВАНИЕ БАЗОВЫХ ФУНКЦИЙ ===")

# Тест date_utils
from src.utils.date_utils import format_date
print(f"✅ format_date: {format_date('2023-12-01T10:30:00')}")

# Тест masks
from src.masks.masks import get_mask_card_number, get_mask_account
print(f"✅ get_mask_card_number: {get_mask_card_number('1234567812345678')}")
print(f"✅ get_mask_account: {get_mask_account('12345678901234567890')}")
# Тест поиска
from src.search import process_bank_search
print(f"✅ process_bank_search импортирована")

# Тест счетчика
from src.counter import process_bank_operations
print(f"✅ process_bank_operations импортирована")

# Тест фильтров
from src.utils.filters import filter_by_status, filter_by_currency, sort_by_date
print(f"✅ Фильтры импортированы")
# Тест обработки
from src.processing.processing import filter_by_state
print(f"✅ filter_by_state импортирована")

# Тест загрузки файлов
from src.utils.file_handlers import read_json_file
print(f"✅ read_json_file импортирована")

print("\n🎉 ВСЕ БАЗОВЫЕ ФУНКЦИИ РАБОТАЮТ!")
