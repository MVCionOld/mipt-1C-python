import collections
import functools


class LruCache:

    def __init__(self, cache_count):
        self.__cache_size = cache_count
        self.__cache = collections.OrderedDict()

    def __contains__(self, key):
        return key in self.__cache

    def __getitem__(self, key):
        return self.__cache.get(key)

    def __setitem__(self, key, value):
        self.__cache[key] = value
        if len(self.__cache) > self.__cache_size:
            self.__cache.popitem(last=False)


def cached(cache_count):
    def wrapped(func):
        lru_cache = LruCache(cache_count)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = tuple(list(args) + list(tuple(kwargs.items())))
            if key not in lru_cache:
                lru_cache[key] = func(*args, **kwargs)
            return lru_cache[key]

        return wrapper

    return wrapped


if __name__ == '__main__':

    @cached(3)
    def fact(n):
        if n < 2:
            return 1
        return fact(n - 1) * n

    print("Call fact(8) =", fact(8), ". Now 6,7,8 are in cache.")
    print("Call fact(7) =", fact(7))
    print("Call fact(6) =", fact(6))
    print("Call fact(5) =", fact(5), "is not in cache!")

    import time
    from functools import lru_cache

    lru_cache_start_time = time.time()


    @lru_cache(5)
    def fact(n):
        if n < 2:
            return 1
        return fact(n - 1) * n


    fact(4)
    fact(8)
    fact(16)
    fact(20)

    lru_cache_end_time = time.time()
    print(f'lru cache benchmark {lru_cache_end_time - lru_cache_start_time}')

    cached_start_time = time.time()


    @cached(5)
    def fact(n):
        if n < 2:
            return 1
        return fact(n - 1) * n


    fact(4)
    fact(8)
    fact(16)
    fact(20)

    cached_end_time = time.time()
    print(f'custom cache benchmark {cached_end_time - cached_start_time}')
