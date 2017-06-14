
from itertools import product
from sympy import Poly, degree

from coding.util import defzip
from .base import Field, Integers

# A note on sympy:
# Sympy is a big library and basically everything (esp. the field stuff) is already
# implemented there. For this reason; we clearly define what will be used from sympy
# and what not. Sympy is used solely for the polynomials and their basic operators,
# just like we use Python for integers and their basic operators.
#
# Polynomials are more than just expressions, they carry their variable with them!

class PolynomialField(Field):
    key = staticmethod(lambda p: degree(p)+1)
    
    def __init__(self, X, F=Integers):
        self.X = X
        self.F = F
        self.one = Poly([F.one], self.X)
        self.zero = Poly([], self.X)
    
    def pad_coeff(self, *polys):
        max_deg = max(map(degree, polys))
        for p in polys:
            coeff = p.all_coeffs()
            yield [self.F.zero] * max(max_deg + 1 - len(coeff), 0) + coeff
    
    def add(self, f, g):
        f_coeff, g_coeff = self.pad_coeff(f, g)
        return Poly((self.F.add(x, y) for x, y in zip(f_coeff, g_coeff)), self.X)
    
    def neg(self, f):
        return Poly((self.F.neg(x) for x in f.all_coeffs()), self.X)
    
    def mul(self, f, g):
        f_coeff, g_coeff = self.pad_coeff(f, g)
        total_coeff = {}
        for i, x in enumerate(reversed(f_coeff)):
            for j, y in enumerate(reversed(g_coeff)):
                total_coeff[i+j] = self.F.add(total_coeff.get(i+j, self.F.zero), self.F.mul(x, y))
        return Poly((total_coeff[i] for i in range(len(total_coeff)-1, -1, -1)), self.X)
    
    def divmod(self, f, g):
        num = f.all_coeffs()
        div = g.all_coeffs()
        
        quot = []
        divisor = div[0]
        for i in range(len(num) - len(div) + 1):
            factor = self.F.div(num[0], divisor)
            quot.append(factor)
            d = [self.F.mul(factor, u) for u in div]
            num = [self.F.sub(u, v) for u, v in defzip(self.F.zero, num, d)]
            if num[0] != self.F.zero:
                raise ValueError(f"Can't divide {f} by {g} in {self.F}")
            num.pop(0)
        
        return Poly(quot, self.X), Poly(num, self.X)
    
    def div(self, f, g):
        return self.divmod(f, g)[0]
    
    def mod(self, f, g):
        return self.divmod(f, g)[1]
    
    def inv(self, f):
        # If this is true:
        #   x**2 + 1     = Poly([1, 0, 1], x)
        # Why something like this?
        #   1/(x**2 + 1) = Poly(      [1, 0, 1], x)
        # ... of course implying the you can retain the variable but the powers can go lower than 0
        raise NotImplemented('Inversion of a Polynomial is not yet defined')
    
    def all_mod(self, f):
        s = set()
        for coeffs in product(*[self.F for _ in range(degree(f))]):
            s.add(self.mod(Poly(coeffs, self.X), f))
        return s
    
    __str__ = __repr__ = lambda s: f'{s.F}[{s.X}]'
    
    def __contains__(self, x):
        return isinstance(x, Poly) \
                and self.X == x.gen \
                and all(c in self.F for c in x.all_coeffs())



import unittest

class IntPolyTests(unittest.TestCase):
    def setUp(self):
        from sympy import Symbol
        self.X = Symbol('X')
        self.PF = PolynomialField(self.X)
    
    def test_simple(self):
        f = Poly([3, 2, -2, 2], self.X)
        g = Poly([1, 0, 4], self.X)
        div, mod = self.PF.divmod(f, g)
        self.assertEqual(div, Poly([3, 2], self.X))
        self.assertEqual(mod, Poly([-14, -6], self.X))
    
    def test_no_div_needed(self):
        f = Poly([1, 2, 3], self.X)
        g = Poly([1, 2, 3, 4], self.X)
        self.assertEqual(self.PF.mod(f, g), f)
    
    def test_undivisable(self):
        f = Poly([10, 0, -4, 2, -2, 2], self.X)
        g = Poly([2, 0, 1, 4], self.X)
        with self.assertRaises(ValueError):
            self.PF.divmod(f, g)


class RealPolyTests(unittest.TestCase):
    def setUp(self):
        from coding.fields.base import Reals
        from sympy import Symbol
        self.X = Symbol('X')
        self.PF = PolynomialField(self.X, Reals)
    
    def test_simple(self):
        f = Poly([10, 0, -4, 2, -2, 2], self.X)
        g = Poly([2, 0, 1, 4], self.X)
        div, mod = self.PF.divmod(f, g)
        self.assertEqual(div, Poly([5, 0, -9/2], self.X))
        self.assertEqual(mod, Poly([-18, 5/2, 20], self.X))

