def read_json(file_path: str):
    """Читает JSON файл с транзакциями"""
    import json
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка чтения файла: {e}")
        return []
