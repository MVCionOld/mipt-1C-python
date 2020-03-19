from functools import (
    reduce,
    wraps
)
from operator import mul


def coroutine(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        generator = func(*args, **kwargs)
        generator.send(None)
        return generator

    return wrapper


@coroutine
def fact_generator(n):
    mult, fact_result = 0, 1
    while mult <= n:
        upper_range = yield fact_result
        if upper_range is not None and upper_range > mult:
            fact_result *= reduce(mul, range(mult+1, upper_range+1))
            mult = upper_range
        elif upper_range is not None:
            raise StopIteration("Attempt to rollback generator state.")
        else:
            mult += 1
            fact_result *= mult


class GeneratorManager:
    
    def __init__(self, *fact_desc):
        self.fact_gens = dict(zip(
            fact_desc,
            list(map(
                fact_generator, 
               fact_desc
            ))
        ))
        for gen_key in self.fact_gens:
            self.fact_gens[gen_key] = (self.fact_gens[gen_key], 1)

    def __len__(self):
        return len(self.fact_gens)

    def send(self, z):
        matched_gen_key, closed_num = -1, 0
        for gen_key in self.fact_gens:
            if gen_key == self.fact_gens[gen_key][1]:
                closed_num += 1
                continue
            elif not(gen_key >= z and self.fact_gens[gen_key][1] < z):
                continue
            if matched_gen_key == -1:
                matched_gen_key = gen_key
            elif self.fact_gens[matched_gen_key][1] < self.fact_gens[gen_key][1]:
                matched_gen_key = gen_key
        if closed_num == len(self):
            print("All generators are closed")
            return None
        elif matched_gen_key == -1:
            print(f"Can't calculate {z}!")
            return None
        self.fact_gens[matched_gen_key] = (
                self.fact_gens[matched_gen_key][0], z
        )
        return self.fact_gens[matched_gen_key][0].send(z)


if __name__ == '__main__':

    f10 = fact_generator(10)
    while True:
        try:
            print(next(f10))
        except StopIteration:
            print("No availability to generate factorials :(")
            break

    print("*"*40)

    f20 = fact_generator(20)
    for i in range(5):
        print(next(f20))
    try:
        print(f20.send(3))
    except Exception as e:
        print(f"{e}")

    print("*"*40)

    gm = GeneratorManager(3, 6)
    print(gm.send(3))
    print(gm.send(3))
    print(gm.send(3))
    print(gm.send(5))
    print(gm.send(7))
    print(gm.send(6))
    print(gm.send(1))







