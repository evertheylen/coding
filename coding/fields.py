
from itertools import product

from coding.util import memoize, euclides

class FiniteField:
    def __init__(self, numbers: set, zero, one, add, opposite, multiply, inverse):
        """Create a finite field. Not meant to be used directly, see modulo_field
        and quotient_field which can construct one for you.
        """
        
        assert zero in numbers
        assert one in numbers
        assert one != zero
        self.numbers = frozenset(numbers)
        self.zero = zero
        self.one = one
        self._add = add
        self._opposite = opposite
        self._multiply = multiply
        self._inverse = inverse
    
    def add(self, x, y):
        return self._add[(x, y)]
    
    def subtract(self, x, y):
        return self.add(x, self.opposite(y))
    
    def opposite(self, x):
        return self._opposite[x]
    
    def multiply(self, x, y):
        return self._multiply[(x, y)]
    
    def divide(self, x, y):
        return self.multiply(x, self.inverse(y))
    
    def inverse(self, x):
        return self._inverse[x]
    
    def __iter__(self):
        return iter(self.numbers)
    
    def __contains__(self, item):
        return item in self.numbers
    
    def check(self):
        "Checks whether this instance of FiniteField is in fact an actual finite field."
        
        ok = True
        for attr, func in type(self).__dict__.items():
            if attr.startswith("check_"):
                res = func(self)
                if not res:
                    print(f"Condition '{func.__doc__}' not met")
                    ok = False
        return ok
    
    def check_add_assoc(self):
        "associativity of addition"
        return all(self.add(self.add(a, b), c) == self.add(a, self.add(b, c))
                   for a, b, c in product(self, self, self))
    
    def check_add_comm(self):
        "commutativity of addition"
        return all(self.add(a, b) == self.add(b, a)
                   for a, b in product(self, self))
    
    def check_add_neutral(self):
        "zero is neutral element for addition"
        return all(self.add(self.zero, a) == a for a in self)
    
    def check_add_opposite(self):
        "every element has an opposite"
        return all(self.add(a, self.opposite(a)) == self.zero for a in self)
    
    def check_mult_assoc(self):
        "associativity of multiplication"
        return all(self.multiply(self.multiply(a, b), c) == self.multiply(a, self.multiply(b, c))
                   for a, b, c in product(self, self, self))
    
    def check_mult_comm(self):
        "commutativity of multiplication"
        return all(self.multiply(a, b) == self.multiply(b, a) 
                   for a, b in product(self, self))
    
    def check_mult_neutral(self):
        "one is neutral element for multiplication"
        return all(self.multiply(self.one, a) == a for a in self)
    
    def check_mult_inverse(self):
        "every element (except 0) has an inverse"
        return all(self.multiply(a, self.inverse(a)) == self.one for a in self if a != self.zero)
    
    def check_distributive(self):
        "addition and multiplication are distributive"
        return all(self.multiply(self.add(a, b), c) == self.add(self.multiply(a, c), self.multiply(b, c))
                   for a, b, c in product(self, self, self))


@memoize
def integer_field(p):
    """Creates a FiniteField based on integers and modulo. `p` should be prime,
    otherwise Euclides will complain.
    """
    
    numbers = set(range(p))
    add = {(a, b): (a+b) % p for a, b in product(numbers, numbers)}
    multiply = {(a, b): (a*b) % p for a, b in product(numbers, numbers)}
    opposite = {a: (-a) % p for a in numbers}
    # inverse is a bit more difficult...
    # We use the algorithm of Euclides 
    inverse = {}
    for a in numbers - {0}:
        gcd, t, s = euclides(a, p)
        if gcd%p != 1:
            raise ValueError(f"Invalid gcd (= {gcd}), p (= {p}) isn't prime")
        inverse[a] = s % p
    
    return FiniteField(numbers, 0, 1, add, opposite, multiply, inverse)




import unittest

class FiniteFieldTest(unittest.TestCase):
    def test_integer_fields(self):
        for p in [2, 3, 7, 11, 97]:
            ff = integer_field(p)
            self.assertTrue(ff.check())
    
    def test_integer_fields_not_prime(self):
        for p in [4, 8, 100]:
            with self.assertRaises(ValueError):
                ff = integer_field(p)
    
    def test_field_check_add(self):
        ff = integer_field(17)
        ff._add[(1, 2)] = 0
        self.assertFalse(ff.check())
    
    def test_field_check_mult(self):
        ff = integer_field(19)
        ff._multiply[(3, 2)] = 18
        self.assertFalse(ff.check())
