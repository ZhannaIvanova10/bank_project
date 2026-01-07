import json


def read_json_file(file_path: str) -> list[dict]:
    """
    Читает JSON-файл и возвращает список транзакций.

    :param file_path: Путь к JSON-файлу.
    :return: Список транзакций или пустой список в случае ошибки.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Файл должен содержать список транзакций.")
            return data
    except (json.JSONDecodeError, FileNotFoundError, ValueError):
        return []
