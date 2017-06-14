
from sympy import Symbol, degree, Poly as _Poly

__all__ = ['Symbol', 'Poly', 'degree']

# A note on sympy:
# Sympy is a big library and basically everything (esp. the field stuff) is already
# implemented there. For this reason; we clearly define what will be used from sympy
# and what not. Sympy is used solely for the polynomials and their basic operators,
# just like we use Python for integers and their basic operators.
#
# Polynomials are more than just expressions, they carry their variable with them!

class Poly(_Poly):
    def __str__(self):
        return str(self.as_expr())
