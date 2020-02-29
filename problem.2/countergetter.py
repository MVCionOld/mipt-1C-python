import collections


class CounterGetter:
    __attrs_counter = collections.defaultdict(int)

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __getattribute__(self, attr):
        CounterGetter.__attrs_counter[attr] += 1
        return super(CounterGetter, self).__getattribute__(attr)

    def __getitem__(self, attr: str):
        return CounterGetter.__attrs_counter[attr]

    def __repr__(self):
        return str(CounterGetter.__attrs_counter)


if __name__ == '__main__':

    import string

    cg1 = CounterGetter(arg0=1, arg1=20)
    cg2 = CounterGetter(
        arg0=2,
        arg1=15,
        arg2="SECRET_KEY",
        arg3=set(string.ascii_lowercase)
    )

    print(cg1)
    print(cg2)
    print(cg2['arg4'])
    cg1.arg0 += cg2.arg1
    print(cg1)
    print(cg2)
    cg1.arg4 = list()
    cg1.arg4.extend([3, 1, 4, 1, 5, 9])
    cg2.arg3.add(cg1.arg1)
    print(cg1)
    print(cg2)
