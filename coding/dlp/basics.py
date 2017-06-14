
import math
from coding.fields import Integers

def bits(n):
    while n:
        b = n & (~n+1)
        yield b
        n ^= b


def powermod(g, n: int, p, F=Integers):
    "Calculates g**n (mod p). g and p should be part of F."
    assert g in F
    assert p in F
    
    powers = list(bits(n))
    results = [F.mod(F.pow(g, i), p) for i in powers]
    res = F.one
    for r in results:
        res = F.mod(F.mul(res, r), p)
    return res
    


import unittest

class DlpTests(unittest.TestCase):
    def test_bits(self):
        self.assertEqual(list(bits(221)), [1, 4, 8, 16, 64, 128])
    
    def test_powermod(self):
        self.assertEqual(powermod(113, 221, 310), 193)
