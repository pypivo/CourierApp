import inspect
import asyncio
from functools import wraps

from fastapi.exceptions import HTTPException

def limiter(max_requests: int = 10, seconds: int = 1):

    def decorator(func):
        rate_limiter = {"count": 0, "last_updated": None}

        @wraps(func)
        async def wrapper(*args, **kwargs):
            nonlocal rate_limiter
            current_time = asyncio.get_running_loop().time()

            # Если прошло достаточно времени, сбрасываем счетчик.
            if rate_limiter["last_updated"] is None or current_time - rate_limiter["last_updated"] >= seconds:
                rate_limiter["count"] = 0

            # Если достигнут лимит запросов, вызываем исключение.
            if rate_limiter["count"] >= max_requests:
                raise HTTPException(status_code=429)

            # Вызываем оригинальную функцию и увеличиваем счетчик запросов.
            result = await func(*args, **kwargs)
            rate_limiter["count"] += 1
            rate_limiter["last_updated"] = current_time

            return result
        return wrapper
    return decorator
