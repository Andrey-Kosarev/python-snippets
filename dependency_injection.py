import random
from typing import Callable


def value_generator():
    return random.randint(1, 100)


def dependency_injector(**fs: Callable):
    def inner(func):
        def wrapper(*args, **kwargs):
            di_args = {k: v() for k, v in fs.items()}
            result = func(*args, **{**di_args, **kwargs})
            return result

        return wrapper

    return inner


@dependency_injector(dep=value_generator)
def func(dep):
    print(f"func received {dep=}")


@dependency_injector(dep=value_generator)
def func_2(val, dep):
    print(f"func2 received {dep=}, {val=}")


@dependency_injector(value=value_generator, value2=value_generator)
def func_3(value, value2):
    print(f"func2 received {value=}, {value2=}")


# USAGE
# simple injection
for _ in range(5):
    func()

# combine injection with arguments
func_2(5)

# overwrite the dependency injection when needed
func_3(value2=15)
func_3(value=0, value2=15)
