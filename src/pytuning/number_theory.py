#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 09:36:58 2016

@author: mark
"""

__all__ = ["odd_limit", "prime_limit", "find_prime_limit_for_scale","find_odd_limit_for_scale"]

from sympy.ntheory.factor_ import factorint

# The Odd-Limit

odd_limit = lambda i: max([x for x in [i.q,i.p] if x %2 != 0])
odd_limit.__doc__ = '''
Find the odd-limit of an interval.

:param i: The interval (a ``sympy.Rational``)
:returns: The odd-limit for the interval.
'''

# Prime-limit

prime_limit = lambda i: max(
            [list(factorint(x).keys()) for x in [i.p,i.q] if x %2 !=0])[0]
prime_limit.__doc__ = '''
Find the prime-limit of an interval.

:param i: The interval (a ``sympy.Rational``)
:returns: The prime-limit for the interval.
'''

# Note that we assume the scale to be book-ended by 1 and 2, so we drop them.

find_prime_limit_for_scale = lambda s: max([prime_limit(x) for x in s[1:-1]])
find_prime_limit_for_scale.__doc__ = '''
Find the prime-limit of an interval.

:param s: The scale (a list of ``sympy.Rational`` values)
:returns: The prime-limit for the scale.
'''

find_odd_limit_for_scale   = lambda s: max([odd_limit(x)   for x in s[1:-1]])
find_odd_limit_for_scale.__doc__ = '''
Find the odd-limit of an interval.

:param s: The scale (a list of ``sympy.Rational`` values)
:returns: The odd-limit for the scale.
'''