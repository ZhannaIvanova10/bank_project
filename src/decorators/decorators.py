from collections.abc import Callable
from typing import Any, Optional
from functools import wraps

def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования работы функций.
    
    :param filename: Имя файла для записи логов (если None, логи выводятся в консоль).
    :return: Декорированная функция.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"
                if filename:
                    with open(filename, "a") as f:
                        f.write(message + "\n")
                else:
                    print(message)
                return result
            except Exception as e:
                message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                if filename:
                    with open(filename, "a") as f:
                        f.write(message + "\n")
                else:
                    print(message)
                raise
        return wrapper
    return decorator
