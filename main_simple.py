"""
Основная программа для домашнего задания 13.2.
Реализует CLI интерфейс для работы с банковскими транзакциями.
"""

import json
import os
import re
import sys
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional

# ============================================================================
# ОСНОВНЫЕ ФУНКЦИИ ИЗ ЗАДАНИЯ
# ============================================================================


def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
    """
    Фильтрует список транзакций по строке поиска в описании.

    Args:
        data: Список словарей с данными о банковских операциях
        search: Строка для поиска (регулярное выражение)

    Returns:
        Отфильтрованный список транзакций
    """
    if not data or not search:
        return []

    result = []
    try:
        pattern = re.compile(search, re.IGNORECASE)
    except re.error:
        pattern = re.compile(re.escape(search), re.IGNORECASE)

    for operation in data:
        description = operation.get("description", "")
        if description and pattern.search(description):
            result.append(operation)

    return result


def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям.

    Args:
        data: Список словарей с данными о банковских операциях
        categories: Список категорий операций

    Returns:
        Словарь, где ключи - категории, значения - количество операций
    """
    if not data:
        return {cat: 0 for cat in categories}

    descriptions = []
    for op in data:
        desc = op.get("description", "")
        if desc:
            descriptions.append(desc.strip())

    category_counts = Counter(descriptions)
    return {cat: category_counts.get(cat, 0) for cat in categories}


# ============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================================


def mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты."""
    card_str = str(card_number)
    digits = "".join(filter(str.isdigit, card_str))

    if len(digits) == 16:
        return f"{digits[:4]} {digits[4:6]}** **** {digits[-4:]}"
    return card_str


def mask_account_number(account: str) -> str:
    """Маскирует номер банковского счета."""
    if not account:
        return ""

    acc_str = str(account)
    digits = "".join(filter(str.isdigit, acc_str))

    if len(digits) >= 4:
        return f"**{digits[-4:]}"
    return acc_str


def format_date(date_str: str) -> str:
    """Форматирует дату в формат DD.MM.YYYY."""
    try:
        if "T" in date_str:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        else:
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


def filter_by_status(data: List[Dict], status: str) -> List[Dict]:
    """Фильтрует транзакции по статусу."""
    if not data:
        return []

    status_lower = status.lower()
    return [op for op in data if op.get("state", "").lower() == status_lower]


def filter_by_currency(data: List[Dict], currency: str = "RUB") -> List[Dict]:
    """Фильтрует транзакции по валюте."""
    if not data:
        return []

    currency_upper = currency.upper()
    filtered = []

    for op in data:
        # Проверяем разные форматы данных
        currency_info = op.get("operationAmount", {}).get("currency", {}) or op.get("currency", {})

        if isinstance(currency_info, dict):
            if currency_info.get("code", "").upper() == currency_upper:
                filtered.append(op)
        elif str(currency_info).upper() == currency_upper:
            filtered.append(op)

    return filtered


def sort_by_date(data: List[Dict], reverse: bool = False) -> List[Dict]:
    """Сортирует транзакции по дате."""
    if not data:
        return []

    def get_date(op: Dict) -> datetime:
        date_str = op.get("date", "")
        try:
            return datetime.fromisoformat(date_str.replace("Z", ""))
        except (ValueError, AttributeError):
            return datetime.min

    return sorted(data, key=get_date, reverse=reverse)


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """Читает данные из JSON-файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка при чтении JSON-файла: {e}")
        return []


# ============================================================================
# ПОЛЬЗОВАТЕЛЬСКИЙ ИНТЕРФЕЙС
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
            masked_from = f"Счет {mask_account_number(acc_str)}"
        else:
            masked_from = mask_card_number(acc_str)
        print(f"⬆ Отправитель: {masked_from}")

    if to_acc:
        acc_str = str(to_acc)
        if "счет" in acc_str.lower():
            masked_to = f"Счет {mask_account_number(acc_str)}"
        else:
            masked_to = mask_card_number(acc_str)
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
            print("⚠ В упрощенной версии поддерживается только JSON")
            return
        elif "XLSX" in file_choice.upper():
            print("\n✅ Для обработки выбран XLSX-файл.")
            data_file = "data/transactions.xlsx"
            print("⚠ В упрощенной версии поддерживается только JSON")
            return
        else:
            print("\n❌ Неизвестный тип файла")
            return
    except Exception as e:
        print(f"\n❌ Ошибка загрузки файла: {e}")
        print("Убедитесь, что файл существует в папке data/")
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

    # Поиск по ключевому слову (ОСНОВНАЯ ФУНКЦИЯ ИЗ ЗАДАНИЯ)
    print("\n" + "=" * 40)
    print("🔎 ПОИСК ПО ОПИСАНИЮ (регулярные выражения)")
    print("=" * 40)
    if get_yes_no("Отфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("\nВведите слово для поиска в описании: ").strip()
        if search_word:
            filtered_data = process_bank_search(filtered_data, search_word)
            print(f"\n🔍 Найдено операций с '{search_word}' в описании: {len(filtered_data)}")

    # Подсчет по категориям (ОСНОВНАЯ ФУНКЦИЯ ИЗ ЗАДАНИЯ)
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
                    if count > 0 and category:
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
