import functools


def checked(*types):
    def wrapped(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for entity in zip(args, types):
                if not isinstance(entity[0], entity[1]):
                    raise TypeError
            return func(*args, **kwargs)

        return wrapper

    return wrapped


if __name__ == '__main__':
    from typing import Dict, List


    @checked(str, int, list)
    def test(a: str, b: int, c: List, d: Dict):
        pass


    test("1", 2, [1], dict(kek="cheburek"))
    test(1, 2, 3, 4)



