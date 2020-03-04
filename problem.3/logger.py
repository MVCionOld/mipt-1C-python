import datetime
import functools
import sys


def singleton(cls):
    instance = None

    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return wrapper


@singleton
class SharedLogger:

    def __init__(self):
        self.record_id = 0

    def __call__(self, func, log_storage, *args, **kwargs):
        time_now_str = str(datetime.datetime.now())
        func_nm_str = func.__name__
        func_out = func(*args, **kwargs)
        log_out_str = "{} {} {} args: {} kwargs: {} result: {}".format(
            self.record_id,
            time_now_str,
            func_nm_str,
            args,
            kwargs,
            func_out
        ).strip() + "\n"
        if log_storage in [sys.stdout, sys.stderr]:
            print(log_out_str, end="\r", file=log_storage)
        else:
            with open(log_storage, 'a') as f:
                f.write(log_out_str)
        self.record_id += 1
        return func_out


def logger(log_storage):
    logger_instance = SharedLogger()

    def wrapped(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return logger_instance(
                func,
                log_storage,
                *args,
                **kwargs
            )

        return wrapper

    return wrapped


if __name__ == '__main__':
    @logger(sys.stderr)
    def test_log_to_stderr(*args, **kwargs):
        return len(args) + len(kwargs)
    @logger('test3.txt')
    def test_log_to_file(*args, **kwargs):
        return len(args) + len(kwargs)
    print(test_log_to_stderr())
    print(test_log_to_file())
    print(test_log_to_stderr(2, mystr="abacaba"))
    print(test_log_to_file(3, myobj=(23, 42)))
