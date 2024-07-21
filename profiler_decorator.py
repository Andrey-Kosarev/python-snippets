from functools import wraps
from cProfile import Profile
from pstats import SortKey


def show_profile_stats(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        prof = Profile()
        result = prof.runcall(fn, *args, **kwargs)
        prof.print_stats(sort=SortKey.CUMULATIVE)
        return result

    return inner

# USAGE
from time import sleep

@show_profile_stats
def i_need_some_optimizeing():
    print("something here is slow")
    sleep(100500)
    return 10
