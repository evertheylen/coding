
from itertools import product

from coding.util import euclides, as_rest_table, Poly, Symbol
from .base import Field, Integers
from .polynomials import PolynomialField


class FiniteField(Field):
    def __init__(self, numbers: set, zero, one, add, neg, mul, inv):
        """Create a finite field. Not meant to be used directly."""
        
        assert zero in numbers
        assert one in numbers
        assert one != zero
        self.numbers = frozenset(numbers)
        self.zero = zero
        self.one = one
        self._add = add
        self._neg = neg
        self._mul = mul
        self._inv = inv
    
    
    # Operations ..........................................
    
    def add(self, x, y):
        return self._add[(x, y)]
    
    def neg(self, x):
        return self._neg[x]
    
    def mul(self, x, y):
        return self._mul[(x, y)]
    
    def inv(self, x):
        return self._inv[x]
    
    def __iter__(self):
        yield self.zero
        yield self.one
        yield from self.numbers - {self.zero, self.one}
    
    def __contains__(self, item):
        return item in self.numbers
    
    def __len__(self):
        return len(self.numbers)
    
    __str__ = __repr__ = lambda s: f'GF({len(s.numbers)})'
    
    
    # Generator and subgroup stuff ........................
    
    def mul_subgroup(self, gen):
        return {self.pow(gen, i) for i in range(len(self))}
    
    def mul_generators(self):
        mul_group = self.numbers - {self.zero}
        return {el for el in self if self.mul_subgroup(el) == mul_group}
    
    
    # Tables and info .....................................
    
    def table_binary(self, op):
        n = list(self)
        data = [[op.__name__] + list(map(str, n))]
        for a in n:
            row = [str(a)]
            for b in n:
                try:
                    row.append(str(op(a, b)))
                except KeyError:
                    row.append('/')
            data.append(row)
        return as_rest_table(data, full=True)
    
    def table_mono(self, op):
        n = list(self)
        data = [[op.__name__] + list(map(str, n)), ['']]
        for a in n:
            try:
                data[1].append(str(op(a)))
            except KeyError:
                data[1].append(' ')
        return as_rest_table(data, full=True)
    
    def table_powers(self, X):
        data = [['pow'] + list(range(len(self))),
                [str(X)] + [str(self.pow(X, i)) for i in range(len(self))]]
        return as_rest_table(data, full=True)
    
    def info(self, X=None):
        s = ''
        s += f"Info for {self}"
        s += '\n' + len(s)*'-'
        s += f"\n\nAddition:\n\n{self.table_binary(self.add)}"
        s += f"\n\nNegation:\n\n{self.table_mono(self.neg)}"
        s += f"\n\nMultiplication:\n\n{self.table_binary(self.mul)}"
        s += f"\n\nInversion:\n\n{self.table_mono(self.inv)}"
        if X: s += f"\n\nPowers:\n\n{self.table_powers(X)}"
        print(s)
    
    
    # Checks validness ....................................
    
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
    
    def check_add_negate(self):
        "every element has an negated version"
        return all(self.add(a, self.neg(a)) == self.zero for a in self)
    
    def check_mult_assoc(self):
        "associativity of multiplication"
        return all(self.mul(self.mul(a, b), c) == self.mul(a, self.mul(b, c))
                   for a, b, c in product(self, self, self))
    
    def check_mult_comm(self):
        "commutativity of multiplication"
        return all(self.mul(a, b) == self.mul(b, a) 
                   for a, b in product(self, self))
    
    def check_mult_neutral(self):
        "one is neutral element for multiplication"
        return all(self.mul(self.one, a) == a for a in self)
    
    def check_mult_inverse(self):
        "every element (except 0) has an inverse"
        return all(self.mul(a, self.inv(a)) == self.one for a in self if a != self.zero)
    
    def check_distributive(self):
        "addition and multiplication are distributive"
        return all(self.mul(self.add(a, b), c) == self.add(self.mul(a, c), self.mul(b, c))
                   for a, b, c in product(self, self, self))

    
    # Constructing with primes ............................

    @classmethod
    def modulo(cls, p, F=Integers):
        """Creates a FiniteField based on modulo. `p` should be prime,
        otherwise Euclides will complain. `p` should also be part of `F`.
        """
        
        assert p in F, f'given prime {p} has to be an element of the given field {F}'
        numbers = F.all_mod(p)
        add = {(a, b): F.mod(F.add(a, b), p) for a, b in product(numbers, numbers)}
        mul = {(a, b): F.mod(F.mul(a, b), p) for a, b in product(numbers, numbers)}
        neg = {a: F.mod(F.neg(a), p) for a in numbers}
        # inverse is a bit more difficult...
        # We use the algorithm of Euclides 
        inv = {}
        for a in numbers - {F.zero}:
            gcd, s, t = euclides(a, p, F)
            gcd = F.mod(gcd, p)
            if F.key(gcd) != 1:
                raise ValueError(f"Invalid gcd (key({gcd}) = {F.key(gcd)} != 1), p (= {p}) isn't prime")
            inv[a] = F.mod(t, p)
        
        return cls(numbers, F.zero, F.one, add, neg, mul, inv)
    
    @classmethod
    def modulo_poly(cls, p, poly, F=Integers):
        """Creates a FiniteField based on polynomials. `p` should be prime.
        `poly` should be an irreducable polynomial in F_p.
        """
        
        F_p = cls.modulo(p, F)
        PF = PolynomialField(poly.gen, F_p)
        return cls.modulo(poly, PF)
        


import unittest

class FiniteFieldTests(unittest.TestCase):
    def test_integer_fields(self):
        for p in [2, 3, 7, 11, 97]:
            ff = FiniteField.modulo(p)
            self.assertTrue(ff.check())
    
    def test_integer_fields_not_prime(self):
        for p in [4, 8, 100]:
            with self.assertRaises(ValueError):
                ff = FiniteField.modulo(p)
    
    def test_field_check_add(self):
        ff = FiniteField.modulo(17)
        ff._add[(1, 2)] = 0
        self.assertFalse(ff.check())
    
    def test_field_check_mult(self):
        ff = FiniteField.modulo(19)
        ff._mul[(3, 2)] = 18
        self.assertFalse(ff.check())
    
    def test_poly_field_16(self):
        g = Poly([1, 0, 0, 1, 1], Symbol('X'))
        ff = FiniteField.modulo_poly(2, g)
        self.assertTrue(ff.check())
    
    def test_poly_field_27(self):
        # https://en.wikipedia.org/wiki/Finite_field#GF.288.29_and_GF.2827.29
        g = Poly([1, 0, 2, 2], Symbol('X'))
        ff = FiniteField.modulo_poly(3, g)
        self.assertTrue(ff.check())
    
    def test_not_poly_field_simple(self):
        g = Poly([1, 0, 1], Symbol('X'))
        with self.assertRaises(ValueError):
            ff = FiniteField.modulo_poly(2, g)

