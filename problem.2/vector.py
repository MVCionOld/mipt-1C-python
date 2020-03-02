import copy
import numbers
import operator


class VectorException(Exception):
    pass


class Vector(list):

    def __init__(self, *args):
        super(Vector, self).__init__(args)

    def __repr__(self):
        return f"Vector{super(Vector, self).__repr__()}"

    def __iadd__(self, other):
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
        result = copy.copy(self)
        result += other
        return result

    def __radd__(self, other):
        return self + other

    def __isub__(self, other):
        self.__iadd__(-other)
        return self

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __imul__(self, other):
        if isinstance(other, numbers.Number):
            for i in range(len(self)):
                self[i] *= other
            return self
        elif isinstance(other, Vector):
            if len(self) != len(other):
                raise VectorException("Unsuitable sizes of operands.")
            else:
                return sum(map(operator.mul, self, other))
        else:
            raise NotImplementedError(f"No mult for {type(other)}")

    def __mul__(self, other):
        if isinstance(other, numbers.Number) or isinstance(other, Vector):
            result = copy.copy(self)
            result *= other
            return result
        else:
            raise NotImplementedError(f"No mult for {type(other)}")

    def __rmul__(self, other):
        return self * other

    def __itruediv__(self, other):
        if isinstance(other, numbers.Number):
            for i in range(len(self)):
                self[i] /= other
            return self
        elif isinstance(other, Vector):
            if len(self) != len(other):
                raise VectorException("Unsuitable sizes of operands.")
            else:
                for i in range(len(self)):
                    self[i] /= other[i]
                return self
        else:
            raise NotImplementedError(f"No div for {type(other)}")

    def __truediv__(self, other):
        result = copy.copy(self)
        if isinstance(other, numbers.Number):
            result /= (Vector(*([1.0]*len(self))) * other)
        else:
            result /= other
        return result

    def __rtruediv__(self, other):
        if isinstance(other, numbers.Number):
            result = (Vector(*([1.0]*len(self))) * other)
        else:
            result = copy.copy(other)
        result /= self
        return result

    def __neg__(self):
        return self * (-1)

    def __pos__(self):
        return self

    def matrix_mult(self, matrix):
        if len(self) != len(matrix):
            raise VectorException("Unsuitable sizes of operands.")
        else:
            return Vector(*(self * Vector(*row) for row in matrix))

    def push_back(self, item):
        self.append(item)

    def pop_back(self):
        self.pop()


if __name__ == '__main__':
    a = Vector(1, 2, 3)
    b = Vector(4, 5, 6)
    c = a + b
    print(a, b, c)
    d = a + 1
    e = 1 + a
    print(a, d, e)
    c = a - 1
    d = 1 - a
    e = c - d
    print(a, c, d, e)
    c = a * b
    d = a * 2
    e = 2 * a
    print(c, d, -e)
    mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    a = Vector(1, 2, 3).matrix_mult(mat)
    print(a)
    a = Vector(3, 1, 4, 1, 5, 9)
    b = a / a
    print(b)
    c = a / 2
    print(c)
    d = 3 / a
    print(d)

