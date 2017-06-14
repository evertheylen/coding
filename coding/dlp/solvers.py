
from itertools import count
import math
from coding.fields import Integers, FiniteField
from coding.util import euclides
from .basics import powermod

class DlpProblem:
    """Given g, G and p, calculate n so that g^n (mod p) = G"""
    
    def __init__(self, g, G, p, F=Integers):
        self.g = g
        self.G = G
        self.p = p
        self.F = F
    

class BruteForce(DlpProblem):
    """Bruteforce solver, runs in O(n)"""
    
    def solve(self):
        n = 0
        _G = self.F.one
        while _G != self.G:
            n += 1
            _G = self.F.mod(self.F.mul(_G, self.g), self.p)
        return n


class BabyStepGaintStep(DlpProblem):
    """Baby step, gaint step. Not in syllabus, reproduced from notes and wikipedia.
    Runs in O(sqrt(n)).
    """
    
    def __init__(self, g, G, p, F=Integers):
        super().__init__(g, G, p, F=F)
        gcd, _, _ = euclides(g, p, F)
        assert gcd == F.one, f"gcd(g, p) should be 1, but gcd({g}, {p}) = {gcd}"

    def solve(self, output=False):
        F = self.F
        m = math.ceil(math.sqrt(self.p))
        if output: print(f"init: m = {m}")
        # Baby steps
        M = {}
        x = F.one  # ascending powers of self.g
        for i in range(m):
            M[F.mod(x, self.p)] = i
            x = F.mod(F.mul(x, self.g), self.p)
        if output: print(f"\n--> Baby steps mapping = {M}")
        
        # Gaint steps
        # (uses little theorem of Fermat: g^(p-1) === 1 (mod p), assumes gcd(g, p) == 1)
        power = F.mod(F.sub(F.neg(m), F.one)
        orig_y = powermod(self.g, power, self.p), self.p, F=F)
        y = F.one
        if output:
            print("\n--> Gaint steps")
            print(f"init: orig_y = {orig_y} = {self.g} ^ {power} (mod {self.p})")
        
        for k in count():  # Will find a solution in m steps
            res = F.mod(F.mul(self.G, y), self.p)
            if output: print(f"Step {k}: result = {res}")
            if res in M:
                if output: print(f"Found solution at step {k}")
                _M = F.from_int(M[res])
                _k = F.from_int(k)
                _m = F.from_int(m)
                return F.mod(F.add(_M, F.mul(_k, _m)), self.p)
            
            y = F.mod(F.mul(y, orig_y), self.p)


# TODO: Pollard, IndexCalculus, Pohlig-Hellman


import unittest

class DlpSolveTests(unittest.TestCase):
    cls = None
    inputs = []  # [(g, n, p)]
    
    def test_solve(self):
        for g, n, p in self.inputs:
            G = powermod(g, n, p)
            _n = self.cls(g, G, p).solve()
            # Don't compare n with _n, since multiple solutions may exist!
            self.assertEqual(powermod(g, _n, p), G)


class BruteForceTests(DlpSolveTests):
    cls = BruteForce
    inputs = [(113, 221, 310),
              (1, 1, 5),
              (12, 23, 34)]

class BabyStepGaintStepTests(DlpSolveTests):
    cls = BabyStepGaintStep
    inputs = [(11, 101, 149)]
    
    def test_not_gcd_1(self):
        with self.assertRaises(AssertionError):
            self.cls(12, 23, 34).solve()
