import numbers
import operator


class VectorException(Exception):
    pass


class Vector(list):

    def __init__(self, *args):
        super(Vector, self).__init__(args)

    def __repr__(self):
        return f"{super(Vector, self).__repr__()}"

    def __iadd__(self, other):
        import pdb; pdb.set_trace()
        if isinstance(other, numbers.Number):
            for i in range(len(self)):
                self[i] += other
            return self
        elif len(self) != len(other):
            raise VectorException("Unsuitable sizes of operands.")
        elif not isinstance(other, Vector):
            raise VectorException("Rhs is not a Vector object.")
        else:
            for i in range(len(self)):
                self[i] += other[i]
            return self

    def __add__(self, other):
        result = Vector(other)
        result += other
        return result

    def __neg__(self):
        return self * (-1)

    def __pos__(self):
        return self

    def __sub__(self, item):
        result = Vector()
        if type(self) == type(item):
            if len(self.massive) == len(item.massive):
                result.massive = list(a - b for a, b in zip(self.massive, item.massive))
            else:
                raise ValueError('ERROR!!! different sizes of Vectors')
        elif type(item) == int or type(item) == float:
            result.massive = []
            for a in self.massive:
                result.massive.append(a - item)
        else:
            raise ValueError('wrong type')
        return result

    def __rsub__(self, vector):
        result = -self
        return result.__radd__(vector)

    # def __getitem__(self, key):
    #     return self.massive[key]

    def push_back(self, item):
        self.append(item)

    def pop_back(self):
        self.pop()

    # def insert(self, index, value):
    #     self.insert(index, value)

    def __imul__(self, other):
        raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return super(Vector, self).__mul__(other)
        elif len(self) != len(other):
            raise VectorException("Unsuitable sizes of operands.")
        elif not isinstance(other, Vector):
            raise VectorException("Rhs is not a Vector object.")
        else:
            return sum(map(operator.mul, self, other))

    def __rmul__(self, other):
        return self * other

    def matrix_mult(self, matrix):
        if len(self) != len(matrix):
            raise VectorException("Unsuitable sizes of operands.")
        else:
            return Vector(*(self * Vector(*row) for row in matrix))


if __name__ == '__main__':
    a = Vector(1, 2, 3)
    b = Vector(4, 5, 6)
    c = a + b
    print(a, b, c)
    d = a + 1
    e = 1 + a
    print(a, d, e)
    # c = a - 1
    # d = 1 - a
    # print(a, c, d)
    # c = a * b
    # d = a * 2
    # e = 2 * a
    # print(c, d, e)
    # mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # a = Vector(1, 2, 3).matrix_mult(mat)
    # print(a)

