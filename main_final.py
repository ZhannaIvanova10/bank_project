"""
Основной модуль для домашнего задания 13.2.
Реализует логику работы с банковскими транзакциями.
"""

import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

# Добавляем путь к модулям проекта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.counter import process_bank_operations
    from src.masks.masks import get_mask_account, get_mask_card_number
    from src.search import process_bank_search
    from src.utils.file_handlers import read_csv_file, read_json_file, read_xlsx_file
    from src.utils.filters import filter_by_currency, filter_by_status, sort_by_date

    # Создаем адаптерные функции
    def mask_card_number(card_number: str) -> str:
        """Адаптер для get_mask_card_number."""
        try:
            return get_mask_card_number(card_number)
        except Exception:
            return str(card_number)

    def mask_account_number(account: str) -> str:
        """Адаптер для get_mask_account."""
        try:
            return get_mask_account(account)
        except Exception:
            return str(account)

    print("✅ Все модули успешно импортированы")

except ImportError as e:
    print(f"❌ Ошибка импорта модулей: {e}")
    import traceback

    traceback.print_exc()
    print("\nПроверьте наличие следующих файлов:")
    print("1. src/utils/file_handlers.py")
    print("2. src/utils/filters.py")
    print("3. src/search.py")
    print("4. src/masks/masks.py")
    print("5. src/counter.py")
    sys.exit(1)


def format_date(date_str: str) -> str:
    """Форматирует дату в формат DD.MM.YYYY."""
    try:
        if "T" in date_str:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        else:
            # Попробуем разные форматы
            for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"):
                try:
                    dt = datetime.strptime(date_str, fmt)
                    break
                except ValueError:
                    continue
            else:
                return date_str
        return dt.strftime("%d.%m.%Y")
    except Exception:
        return date_str


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

    # Дата
    date_str = op.get("date", "")
    if date_str:
        formatted_date = format_date(date_str)
        print(f"📅 Дата: {formatted_date}")

    # Описание
    description = op.get("description", "Без описания")
    print(f"📝 Описание: {description}")

    # Отправитель и получатель
    from_acc = op.get("from", "")
    to_acc = op.get("to", "")

    if from_acc:
        acc_str = str(from_acc)
        if "счет" in acc_str.lower():
            masked_from = f"Счет {mask_account_number(''.join(filter(str.isdigit, acc_str)))}"
        else:
            # Извлекаем цифры для маскировки карты
            digits = "".join(filter(str.isdigit, acc_str))
            masked_from = mask_card_number(digits) if len(digits) == 16 else acc_str
        print(f"⬆ Отправитель: {masked_from}")

    if to_acc:
        acc_str = str(to_acc)
        if "счет" in acc_str.lower():
            masked_to = f"Счет {mask_account_number(''.join(filter(str.isdigit, acc_str)))}"
        else:
            digits = "".join(filter(str.isdigit, acc_str))
            masked_to = mask_card_number(digits) if len(digits) == 16 else acc_str
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

    # Загрузка данных
    data_file = None
    data = []

    try:
        if "JSON" in file_choice.upper():
            print("\n✅ Для обработки выбран JSON-файл.")
            data_file = "data/operations.json"
            data = read_json_file(data_file)
        elif "CSV" in file_choice.upper():
            print("\n✅ Для обработки выбран CSV-файл.")
            data_file = "data/transactions.csv"
            data = read_csv_file(data_file)
        elif "XLSX" in file_choice.upper():
            print("\n✅ Для обработки выбран XLSX-файл.")
            data_file = "data/transactions.xlsx"
            data = read_xlsx_file(data_file)
        else:
            print("\n❌ Неизвестный тип файла")
            return
    except Exception as e:
        print(f"\n❌ Ошибка загрузки файла: {e}")
        print("Убедитесь, что файл существует в папке data/")
        print("Доступные файлы:")
        import os

        if os.path.exists("data"):
            for f in os.listdir("data"):
                print(f"  - data/{f}")
        else:
            print("  Папка data/ не существует")
        return

    print(f"\n📊 Успешно загружено {len(data)} операций.")

    if not data:
        print("\n⚠ Нет данных для обработки.")
        return

    # Фильтрация по статусу
    print("\n" + "=" * 40)
    print("🔍 ФИЛЬТРАЦИЯ ПО СТАТУСУ")
    print("=" * 40)
    status = get_status()

    filtered_data = filter_by_status(data, status)
    print(f"\n✅ Операции отфильтрованы по статусу '{status}'")
    print(f"📈 Найдено операций: {len(filtered_data)}")

    if not filtered_data:
        print("\n⚠ Не найдено ни одной транзакции с указанным статусом.")
        return

    # Сортировка
    print("\n" + "=" * 40)
    print("📅 СОРТИРОВКА")
    print("=" * 40)
    if get_yes_no("Отсортировать операции по дате?"):
        sort_order = get_user_choice(["по возрастанию", "по убыванию"], "Выберите порядок сортировки:")
        reverse_order = sort_order == "по убыванию"

        filtered_data = sort_by_date(filtered_data, reverse_order)
        print(f"\n✅ Операции отсортированы {sort_order}")

    # Фильтрация по валюте
    print("\n" + "=" * 40)
    print("💰 ФИЛЬТРАЦИЯ ПО ВАЛЮТЕ")
    print("=" * 40)
    if get_yes_no("Выводить только рублевые транзакции?"):
        filtered_data = filter_by_currency(filtered_data, "RUB")
        print(f"\n✅ Оставлено рублевых транзакций: {len(filtered_data)}")

    # Поиск по ключевому слову
    print("\n" + "=" * 40)
    print("🔎 ПОИСК ПО ОПИСАНИЮ")
    print("=" * 40)
    if get_yes_no("Отфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("\nВведите слово для поиска в описании: ").strip()
        if search_word:
            filtered_data = process_bank_search(filtered_data, search_word)
            print(f"\n🔍 Найдено операций с '{search_word}' в описании: {len(filtered_data)}")

    # Подсчет по категориям (демонстрация функции)
    if filtered_data:
        print("\n" + "=" * 40)
        print("📊 СТАТИСТИКА ПО КАТЕГОРИЯМ")
        print("=" * 40)
        if get_yes_no("Показать статистику по категориям операций?"):
            # Получаем уникальные категории
            categories = list(set(op.get("description", "") for op in filtered_data if op.get("description")))
            if categories:
                category_stats = process_bank_operations(filtered_data, categories)
                print("\n📈 Статистика по категориям:")
                for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
                    if count > 0 and category:  # Пропускаем пустые категории
                        print(f"  • {category}: {count} операций")

    # Вывод результатов
    print("\n" + "=" * 60)
    print("📄 РЕЗУЛЬТАТЫ ОБРАБОТКИ")
    print("=" * 60)
    print(f"Всего банковских операций в выборке: {len(filtered_data)}")
    print("=" * 60)

    if not filtered_data:
        print("\n⚠ Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
        return

    # Ограничиваем вывод
    max_to_show = min(10, len(filtered_data))
    print(f"\nПоказаны первые {max_to_show} операций:")

    for i in range(max_to_show):
        print_operation(filtered_data[i], i)

    if len(filtered_data) > max_to_show:
        print(f"\n📋 ... и ещё {len(filtered_data) - max_to_show} операций")

    print("\n" + "=" * 60)
    print("🎉 ОБРАБОТКА ЗАВЕРШЕНА! СПАСИБО ЗА ИСПОЛЬЗОВАНИЕ ПРОГРАММЫ!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Программа прервана пользователем.")
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        import traceback

        traceback.print_exc()
EOF
