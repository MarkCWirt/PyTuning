#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 09:36:58 2016

@author: mark
"""

__all__ = ["odd_limit", "prime_limit", "find_prime_limit_for_scale",
           "find_odd_limit_for_scale", "prime_factor_ratio", "create_ratio_from_primes"]

from sympy.ntheory.factor_ import factorint, factorrat, isprime
import sympy as sp

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

def prime_factor_ratio(r, return_as_vector = False):
    '''
    Decompose a ratio (degree) to prime factors
    
    :param r: The degree to factor (``sympy.Rational``)
    :param return_as_vector: If ``True``, return the factors as a vector
        (see below)
    :returns: The factoring of the ratio
    
    By default this function will return a ``dict``, with each key
    being a prime, and each value being the exponent of the factorization.
    
    As an example, the syntonic comma, :math:`\\frac{81}{80}`, can be factored:
        
    .. code:: python
    
        r = syntonic_comma
        q = prime_factor_ratio(r)
        print(q)
        {2: -4, 3: 4, 5: -1}
    
    which can be interpreted as:
        
    .. math::
        
        \\frac{3^4}{2^{4} \cdot 5^{1}}
        
    If ``return_as_vector`` is ``True``, the function will return a tuple, 
    with each position a successive prime. The above example yields:
        
    .. code:: python
    
        r = syntonic_comma
        q = prime_factor_ratio(r, return_as_vector=True)
        print(q)
        (-4, 4, -1)
        
    Note that zeros will be included in the vector, thus:
        
    .. code:: python
    
        r = sp.Rational(243,224)
        q = prime_factor_ratio(r, return_as_vector=True)
        print(q)
        (-5, 5, 0, -1)
        q = prime_factor_ratio(r)
        print(q)
        {2: -5, 3: 5, 7: -1}
    '''
    factors = dict(factorrat(r))
    if return_as_vector:
        f = [x for x in range(max(factors)+1) if isprime(x)]
        output = []
        for index in f:
            item = factors[index] if index in factors else 0
            output.append(item)
        output = tuple(output)
    else:
        output = factors
            
    return output

def create_ratio_from_primes(factors):
    '''
    Given a prime factorization of a ratio, reconstruct the ratio. This function
    in the inverse of :func:`prime_factor_ratio`.
    
    :param factors: The factors. Can be a ``dict`` or a ``tuple`` 
        (see ``prime_factor_ratio`` for a discussion).
    :returns: The ratio (``sympy`` value).
    '''
    if type(factors) == tuple:
        internal_factors = {}
        f = []
        f_try = 2
        while len(f) < len(factors):
            if isprime(f_try):
                f.append(f_try)
            f_try = f_try + 1
        for index in range(len(factors)):
            internal_factors[f[index]] = factors[index]
    else:
        internal_factors = factors
    output = sp.Integer(1)
    for k, v in internal_factors.items():
        output = output * sp.power.Pow(k, v)
    return output

