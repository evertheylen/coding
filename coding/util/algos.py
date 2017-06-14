
from coding.util.table import as_rest_table

__all__ = ['euclides']

def euclides(a: int, b: int, F=None, output=False) -> 'd, s, t':
    """Algorithm of Euclides. Given two numbers `a` and `b`, calculates their greatest
    common denominator `d`, and tells you how to write `d` as `s*a + t*b`.
    """
    
    if F is None:  # avoid circular imports
        from coding.fields.base import Integers
        F = Integers
    
    r = {0: max(a, b, key=F.key),
         1: min(a, b, key=F.key)}
    s = {0: F.one, 1: F.zero}
    t = {0: F.zero, 1: F.one}
    
    i = 1
    while r[i] != F.zero:
        quotient, r[i+1] = F.divmod(r[i-1], r[i])
        s[i+1] = F.add(F.mul(F.neg(quotient), s[i]), s[i-1])
        t[i+1] = F.add(F.mul(F.neg(quotient), t[i]), t[i-1])
        i += 1
    
    if output:
        data = [['i', 's', 't', 'r']]
        for k in range(i):
            data.append([str(k), str(s[k]), str(t[k]), str(r[k])])
        print(f"Euclides algo, given a = {a}, b = {b}")
        print()
        print(as_rest_table(data))
    
    if r[i-1] != F.one:
        return F.neg(r[i-1]), F.neg(s[i-1]), F.neg(t[i-1])
    else:
        return r[i-1], s[i-1], t[i-1]
