
from .table import as_rest_table

def euclides(a: int, b: int, output=False) -> 'd, t, s':
    """Algorithm of Euclides. Given two numbers `a` and `b`, calculates their greatest
    common denominator `d`, and tells you how to write `d` as `t*a + s*b`.
    """
    
    r = {0: max(abs(a), abs(b)),
         1: min(abs(a), abs(b))}
    t = {0: 1, 1: 0}
    s = {0: 0, 1: 1}
    
    i = 1
    while r[i] != 0:
        quotient = r[i-1] // r[i]
        r[i+1] = r[i-1] % r[i]
        t[i+1] = -quotient*t[i] + t[i-1]
        s[i+1] = -quotient*s[i] + s[i-1]
        i += 1
    
    if output:
        data = [['i', 't', 's', 'r']]
        for k in range(i):
            data += [[k, s[k], r[k], t[k]]]
        print(f"Euclides algo, given a = {a}, b = {b}")
        print()
        print(as_rest_table(data))
    
    return r[i-1], t[i-1], s[i-1]
