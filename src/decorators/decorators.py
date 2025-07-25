from typing import Callable, Optional, Any
import datetime
import functools


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызовов функций

    :param filename: Имя файла для логирования (None - вывод в консоль)
    :return: Декорированная функция
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                result = func(*args, **kwargs)
                log_message = f"{timestamp} {func.__name__} ok\n"
                if filename:
                    with open(filename, "a") as f:
                        f.write(log_message)
                else:
                    print(log_message, end="")
                return result
            except Exception as e:
                log_message = f"{timestamp} {func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"
                if filename:
                    with open(filename, "a") as f:
                        f.write(log_message)
                else:
                    print(log_message, end="")
                raise

        return wrapper

    return decorator
