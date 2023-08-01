import os
from functools import wraps
from typing import Callable

import diskcache

CACHE_DIR = '.diskcache'

# if os.access(CACHE_DIR, os.W_OK):
cache = diskcache.Cache(CACHE_DIR)
use_cache = True
# use_cache = False
# else:
#     use_cache = False


def memoize_cache(f: Callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if use_cache:
            key = (args, tuple(sorted(kwargs.items())))
            result = cache.get(key)
            if result is None:
                result = f(*args, **kwargs)
                cache.set(key, result)
            return result
        else:
            return f(*args, **kwargs)

    return wrapper


def should_use_cache():
    return use_cache


def get_from_cache(key):
    return cache.get(key)


def set_in_cache(key, value):
    return cache.set(key, value)
