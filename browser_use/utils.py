import logging
import time
from functools import wraps
from typing import Any, Callable, Coroutine, TypeVar

logger = logging.getLogger(__name__)


# Define generic type variables for return type
R = TypeVar('R')


def time_execution_sync(additional_text: str = '') -> Callable[..., Callable[..., R]]:
    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.debug(f'{additional_text} Execution time: {execution_time:.2f} seconds')
            return result

        return wrapper

    return decorator


def time_execution_async(
    additional_text: str = '',
) -> Callable[..., Callable[..., Coroutine[Any, Any, R]]]:
    def decorator(func: Callable[..., Coroutine[Any, Any, R]]) -> Callable[..., Coroutine[Any, Any, R]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> R:
            start_time = time.time()
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.debug(f'{additional_text} Execution time: {execution_time:.2f} seconds')
            return result

        return wrapper

    return decorator


def singleton(cls):
    instance = [None]

    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper
