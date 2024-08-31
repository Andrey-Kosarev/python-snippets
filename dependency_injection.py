import random
from typing import Callable


def value_generator():
    return random.randint(1, 5)


def dependency_injector(**fs: Callable):
    def inner(func):
        def wrapper(*args, **kwargs):
            di_args = {k:v() for k, v in fs.items() }
            result = func(*args, **kwargs, **di_args)
            return result
        return wrapper
    return inner


@dependency_injector(dep=value_generator)
def func(dep):
    print(f"func received {dep=}")


@dependency_injector(dep=value_generator)
def func_2(val, dep):
    print(f"func2 received {dep=}, {val=}")


for _ in range(10):
    func()


func_2(5)