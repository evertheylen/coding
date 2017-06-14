
import math

__all__ = ['Field', 'Reals', 'Integers']

class Field:
    # Minimally; implement add, neg, mul, inv
    # If possible, also implement all_mod, __iter__ and __contains__
    
    # for use in max and min
    key = staticmethod(lambda x: x)
    
    def sub(self, x, y):
        return self.add(x, self.neg(y))
    
    def div(self, x, y):
        return self.mul(x, self.inv(y))
    
    def mod(self, x, y):
        return self.sub(x, self.div(x, y))
    
    def divmod(self, x, y):
        return self.div(x, y), self.mod(x, y)
    
    def pow(self, x, n: int):
        res = self.one
        for i in range(n):
            res = self.mul(res, x)
        return res
    
    def all_mod(self, x):
        s = set()
        for i in self:
            s.add(self.mod(i, x))
        return s
    
    def from_int(self, i: int):
        res = self.zero
        for i in range(i):
            res = self.add(res, self.one)
        return res
    
    def __len__(self):
        return float('inf')


class _RealField(Field):
    one = 1
    zero = 0
    
    def add(self, x, y):
        return x + y
    
    def sub(self, x, y):
        return x - y
    
    def neg(self, x):
        return -x
    
    def mul(self, x, y):
        return x * y
    
    def pow(self, x, n):
        return math.pow(x, n)
    
    def div(self, x, y):
        return x / y
    
    def inv(self, x):
        return 1 / x
    
    def mod(self, x, y):
        return 0
    
    def from_int(self, i):
        return float(i)
    
    def __contains__(self, x):
        try:
            return float('-inf') <= x <= float('inf')
        except TypeError:
            return False
    
    __str__ = __repr__ = lambda s: 'Reals'
        

Reals = _RealField()


class _IntegerField(_RealField):
    def pow(self, x, n):
        return pow(x, n)

    def div(self, x, y):
        return x // y
    
    def mod(self, x, y):
        return x % y
    
    def all_mod(self, x):
        return set(range(x))
    
    def from_int(self, i):
        return i
    
    def __contains__(self, x):
        try:
            return x % 1 == 0
        except TypeError:
            return False
    
    __str__ = __repr__ = lambda s: 'Integers'

Integers = _IntegerField()

