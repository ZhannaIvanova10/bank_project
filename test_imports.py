# Проверка импортов с правильными именами
try:
    from src.masks.masks import get_mask_card_number, get_mask_account
    print("✅ masks.py: get_mask_card_number, get_mask_account")
except ImportError as e:
    print(f"❌ masks.py: {e}")

try:
    from src.utils.date_utils import format_date
    print("✅ date_utils.py: format_date")
except ImportError as e:
    print(f"❌ date_utils.py: {e}")

try:
    from src.utils.file_handlers import read_json_file, read_csv_file, read_xlsx_file
    print("✅ file_handlers.py: read_json_file, read_csv_file, read_xlsx_file")
except ImportError as e:
    print(f"❌ file_handlers.py: {e}")

try:
    from src.utils.filters import filter_by_status, filter_by_currency
    print("✅ filters.py: filter_by_status, filter_by_currency")
except ImportError as e:
    print(f"❌ filters.py: {e}")

try:
    from src.processing.processing import sort_by_date, filter_by_state
    print("✅ processing.py: sort_by_date, filter_by_state")
except ImportError as e:
    print(f"❌ processing.py: {e}")

try:
    from src.search import process_bank_search
    print("✅ search.py: process_bank_search")
except ImportError as e:
    print(f"❌ search.py: {e}")

try:
    from src.counter import process_bank_operations
    print("✅ counter.py: process_bank_operations")
except ImportError as e:
    print(f"❌ counter.py: {e}")