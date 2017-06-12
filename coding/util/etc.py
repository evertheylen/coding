"""Various small utilities, not directly related to coding theory.
"""

from functools import update_wrapper
from collections import defaultdict

class memoize(dict):
    "Memoization decorator for functions taking one or more arguments."
    def __init__(self, f):
        self.f = f
        update_wrapper(self, f)
        
    def __call__(self, *args):
        return self[args]
    
    def __missing__(self, key):
        ret = self[key] = self.f(*key)
        return ret


class multimap(defaultdict):
    def __init__(self, *a, **kw):
        super().__init__(set, *a, **kw)
    
    def flat_items(self):
        for k, values in self.items():
            for v in values:
                yield k, v
                
    def flat_values(self):
        for values in self.values():
            for v in values:
                yield v
    
    def flat_len(self):
        s = 0
        for v in self.values():
            s += len(v)
        return s
    
    def flatten(self):
        d = {}
        for k, v in self.items():
            if len(v) != 1:
                raise NotFlat(v)
            d[k] = v.pop()
        return d
