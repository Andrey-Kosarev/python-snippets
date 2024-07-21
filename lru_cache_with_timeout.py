from datetime import datetime, timedelta


def lru_timed_cache(timeout: int, max_size: int = 10):
    """decorator fabric which stored cache of {max_items} latest calls of a function for {seconds} seconds"""

    def get_args_hash(args, kwargs):
        args_tuple = tuple(args)
        kwargs_tuple = tuple(sorted(kwargs.items()))
        return hash((args_tuple, kwargs_tuple))

    def wrapper(fn):
        cache = dict()  # {"${arg_hash}":  {"cache_ts": datetime(), "value": value}}

        def inner(*args, **kwargs):
            now = datetime.now()
            args_hash = get_args_hash(args, kwargs)
            cached_value = cache.get(args_hash)

            if not cached_value or (cached_value["cache_ts"] + timedelta(seconds=timeout) < now):
                result = fn(*args, **kwargs)
                cache[args_hash] = {"cache_ts": datetime.now(), "value": result}
            else:
                result = cached_value.get("value")

            if len(cache) > max_size:
                latest_cache = sorted(cache.items(), key=lambda c: c[1]['cache_ts'], reverse=True)[:max_size]
                cache.clear()
                cache.update(latest_cache)

            return result

        return inner

    return wrapper


# USAGE 
import time

@lru_timed_cache(timeout=60*60, max_size=256)
def super_long_function():
    print("doing super long stuff")
    time.sleep(100)
    return 10
