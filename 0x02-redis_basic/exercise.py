from typing import Callable, Optional, Union
from uuid import uuid4
import redis
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of times a method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for counting calls."""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a particular function."""
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function for storing call history."""
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper

def replay(method: Callable) -> None:
    """
    Replays the history of a function.
    Args:
        method: The function to replay history for.
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = int(cache.get(name).decode("utf-8"))
    print(f"{name} was called {calls} times:")
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for inp, outp in zip(inputs, outputs):
        print(f"{name}(*{inp.decode('utf-8')}) -> {outp.decode('utf-8')}")

class Cache:
    """Cache class for storing and retrieving data."""
    def __init__(self):
        """Initialize the cache."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in the cache and return a unique key."""
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Get data from the cache by key, optionally applying a transformation function."""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Get a string from the cache by key."""
        value = self._redis.get(key)
        return value.decode('utf-8')

    def get_int(self, key: str) -> int:
        """Get an integer from the cache by key."""
        value = self._redis.get(key)
        try:
            value = int(value.decode('utf-8'))
        except Exception:
            value = 0
        return value

# Example usage:
if __name__ == "__main__":
    cache = Cache()
    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    replay(cache.store)
