"""
Основная программа для домашнего задания 13.2.
Объединяет весь функционал из домашних заданий 9.1-13.2.
"""
import re
from typing import List, Dict, Any, Optional

# ============================================================================
# ИМПОРТ ФУНКЦИЙ ИЗ МОДУЛЕЙ (прямые импорты)
# ============================================================================

# Из задания 9.2 - маскировка и форматирование даты
from src.masks.masks import get_mask_card_number, get_mask_account
from src.utils.date_utils import format_date
# Из заданий 12.1 и 13.1 - чтение файлов
from src.utils.file_handlers import read_json_file, read_csv_file, read_xlsx_file

# Из заданий 10.1 и 11.1 - фильтрация и сортировка
from src.utils.filters import filter_by_status, filter_by_currency, sort_by_date

# Из задания 10.1 - альтернативная фильтрация по статусу
from src.processing.processing import filter_by_state

# Из задания 13.2 - основные функции
from src.search import process_bank_search
from src.counter import process_bank_operations


# ============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ (только UI)
# ============================================================================

def get_user_choice(options: List[str], prompt: str) -> str:
    """Получает выбор пользователя с валидацией."""
    while True:
        print(f"\n{prompt}")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        choice = input("Ваш выбор (введите номер): ").strip()

        if choice.isdigit():
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                return options[choice_num - 1]

        print(f"⚠ Пожалуйста, введите число от 1 до {len(options)}")

def get_yes_no(prompt: str) -> bool:
    """Получает ответ Да/Нет."""
    while True:
        answer = input(f"\n{prompt} (Да/Нет): ").strip().lower()

        if answer in ["да", "yes", "д", "y", "+"]:
            return True
        elif answer in ["нет", "no", "н", "n"]:
            return False

        print("⚠ Пожалуйста, ответьте 'Да' или 'Нет'")


def get_status() -> str:
    """Получает статус операции."""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print(f"\nВведите статус операции для фильтрации.")
        print(f"Доступные статусы: {', '.join(valid_statuses)}")

        status = input("Статус: ").strip().upper()

        if status in valid_statuses:
            return status

        print(f'❌ Статус операции "{status}" недоступен. Попробуйте снова.')


def print_operation(op: Dict[str, Any], index: Optional[int] = None):
    """Форматированный вывод одной операции."""
    if index is not None:
        print(f"\n{'=' * 50}")
        print(f"ОПЕРАЦИЯ #{index + 1}")
        print(f"{'=' * 50}")

    # Дата (из задания 9.2)
    date_str = op.get("date", "")
    if date_str:
        formatted_date = format_date(date_str)
        print(f"📅 Дата: {formatted_date}")

    # Описание
    description = op.get("description", "Без описания")
    print(f"📝 Описание: {description}")

    # Отправитель и получатель (из задания 9.2)
    from_acc = op.get("from", "")
    to_acc = op.get("to", "")

    if from_acc:
        acc_str = str(from_acc)
        if "счет" in acc_str.lower():
            masked_from = f"Счет {get_mask_account(acc_str)}"
        else:
            masked_from = get_mask_card_number(acc_str)
        print(f"⬆ Отправитель: {masked_from}")
    if to_acc:
        acc_str = str(to_acc)
        if "счет" in acc_str.lower():
            masked_to = f"Счет {get_mask_account(acc_str)}"
        else:
            masked_to = get_mask_card_number(acc_str)
        print(f"⬇ Получатель: {masked_to}")

    # Сумма и валюта
    amount = op.get("amount", 0)
    operation_amount = op.get("operationAmount", {})

    if operation_amount and isinstance(operation_amount, dict):
        amount = operation_amount.get("amount", amount)
        currency_info = operation_amount.get("currency", {})
    else:
        currency_info = op.get("currency", {})
    if isinstance(currency_info, dict):
        currency_code = currency_info.get("code", "RUB")
        currency_name = currency_info.get("name", "")
    else:
        currency_code = str(currency_info)
        currency_name = ""

    currency_display = f"{currency_code}"
    if currency_name:
        currency_display += f" ({currency_name})"

    print(f"💰 Сумма: {amount} {currency_display}")

    # Статус
    state = op.get("state", "UNKNOWN")
    status_icon = "✅" if state == "EXECUTED" else "❌" if state == "CANCELED" else "⏳"
    print(f"{status_icon} Статус: {state}")
def load_transactions(file_type: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из файла выбранного типа.
    Использует функции из заданий 12.1 и 13.1.
    """
    if file_type.lower() == 'json':
        return read_json_file('data/operations.json')
    elif file_type.lower() == 'csv':
        return read_csv_file('data/transactions.csv')
    elif file_type.lower() == 'xlsx':
        return read_xlsx_file('data/transactions.xlsx')
    else:
        print("❌ Неподдерживаемый тип файла")
        return []
# ============================================================================
# ОСНОВНАЯ ЛОГИКА ПРОГРАММЫ
# ============================================================================

def main():
    """Основная функция программы."""
    print("=" * 60)
    print("🏦 ПРИВЕТСТВУЕМ В ПРОГРАММЕ РАБОТЫ С БАНКОВСКИМИ ТРАНЗАКЦИЯМИ!")
    print("=" * 60)

    # Выбор типа файла
    file_options = [
        "Получить информацию о транзакциях из JSON-файла",
        "Получить информацию о транзакциях из CSV-файла",
        "Получить информацию о транзакциях из XLSX-файла",
    ]

    file_choice = get_user_choice(file_options, "📂 Выберите тип файла для загрузки:")

    # Определяем тип файла и загружаем данные
    data = []
    try:
        if "JSON" in file_choice.upper():
            print("\n✅ Для обработки выбран JSON-файл.")
            data = load_transactions('json')
        elif "CSV" in file_choice.upper():
            print("\n✅ Для обработки выбран CSV-файл.")
            data = load_transactions('csv')
        elif "XLSX" in file_choice.upper():
            print("\n✅ Для обработки выбран XLSX-файл.")
            data = load_transactions('xlsx')
        else:
            print("\n❌ Неизвестный тип файла")
            return
    except Exception as e:
        print(f"\n❌ Ошибка загрузки файла: {e}")
        print("Убедитесь, что файлы существуют в папке data/")
        print("Нужные файлы: operations.json, transactions.csv, transactions.xlsx")
        return

    print(f"\n📊 Успешно загружено {len(data)} операций.")
    if not data:
        print("\n⚠ Нет данных для обработки.")
        return

    # 1. Фильтрация по статусу (из задания 10.1)
    print("\n" + "=" * 40)
    print("🔍 ФИЛЬТРАЦИЯ ПО СТАТУСУ")
    print("=" * 40)
    status = get_status()

    # Используем filter_by_state из src/processing/processing.py
    filtered_data = filter_by_state(data, status)
    print(f"\n✅ Операции отфильтрованы по статусу '{status}'")
    print(f"📈 Найдено операций: {len(filtered_data)}")

    if not filtered_data:
        print("\n⚠ Не найдено ни одной транзакции с указанным статусом.")
        return
    # 2. Сортировка по дате (из задания 10.1)
    print("\n" + "=" * 40)
    print("📅 СОРТИРОВКА")
    print("=" * 40)
    if get_yes_no("Отсортировать операции по дате?"):
        sort_order = get_user_choice(["по возрастанию", "по убыванию"], "Выберите порядок сортировки:")
        reverse_order = sort_order == "по убыванию"

        # Используем sort_by_date из src/utils/filters.py
        filtered_data = sort_by_date(filtered_data, reverse_order)
        print(f"\n✅ Операции отсортированы {sort_order}")

    # 3. Фильтрация по валюте (из задания 11.1)
    print("\n" + "=" * 40)
    print("💰 ФИЛЬТРАЦИЯ ПО ВАЛЮТЕ")
    print("=" * 40)
    if get_yes_no("Выводить только рублевые транзакции?"):
        # Используем filter_by_currency из src/utils/filters.py
        filtered_data = filter_by_currency(filtered_data, "RUB")
        print(f"\n✅ Оставлено рублевых транзакций: {len(filtered_data)}")
    # 4. Поиск по описанию (ОСНОВНАЯ ФУНКЦИЯ из задания 13.2)
    print("\n" + "=" * 40)
    print("🔎 ПОИСК ПО ОПИСАНИЮ (регулярные выражения)")
    print("=" * 40)
    if get_yes_no("Отфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("\nВведите слово для поиска в описании: ").strip()
        if search_word:
            # Используем process_bank_search из src/search.py
            filtered_data = process_bank_search(filtered_data, search_word)
            print(f"\n🔍 Найдено операций с '{search_word}' в описании: {len(filtered_data)}")

    # 5. Статистика по категориям (ОСНОВНАЯ ФУНКЦИЯ из задания 13.2)
    if filtered_data:
        print("\n" + "=" * 40)
        print("📊 СТАТИСТИКА ПО КАТЕГОРИЯМ")
        print("=" * 40)
        if get_yes_no("Показать статистику по категориям операций?"):
            # Получаем уникальные категории
            categories = list(set(op.get("description", "") for op in filtered_data if op.get("description")))
            if categories:
                # Используем process_bank_operations из src/counter.py
                category_stats = process_bank_operations(filtered_data, categories)
                print("\n📈 Статистика по категориям:")
                for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
                    if count > 0 and category:
                        print(f"  • {category}: {count} операций")

    # 6. Вывод результатов с форматированием (из задания 9.2)
    print("\n" + "=" * 60)
    print("📄 РЕЗУЛЬТАТЫ ОБРАБОТКИ")
    print("=" * 60)
    print(f"Всего банковских операций в выборке: {len(filtered_data)}")
    print("=" * 60)
    if not filtered_data:
        print("\n⚠ Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    # Ограничиваем вывод
    max_to_show = min(5, len(filtered_data))
    print(f"\nПоказаны первые {max_to_show} операций:")

    for i in range(max_to_show):
        print_operation(filtered_data[i], i)

    if len(filtered_data) > max_to_show:
        print(f"\n📋 ... и ещё {len(filtered_data) - max_to_show} операций")

    print("\n" + "=" * 60)
    print("🎉 ОБРАБОТКА ЗАВЕРШЕНА! СПАСИБО ЗА ИСПОЛЬЗОВАНИЕ ПРОГРАММЫ!")
    print("=" * 60)
# ============================================================================
# ТОЧКА ВХОДА
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Программа прервана пользователем.")
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()
