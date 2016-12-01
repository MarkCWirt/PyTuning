#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 10:36:33 2016

@author: mark
"""

import sympy as sp

def create_diatonic_scale(generators, specification):
    '''
    Create a diatonic scale.
    
    :param generators: The generator intervals (see below)
    :param specification: The scale specification. This is a list
        of ``chars`` that correspond to entries in the generators. Note that
        if all the character representations are a single character, you can
        pass the specification in as a string for convenience.
    :returns: The specified scale
    
    ``generators`` is a list of tuples, the first member of which is an interval
    specification, the second of which is a character representation. The entries
    in ``specification`` should correspond to this value.
    
    As an example, we can create the 12 EDO generators thus:
    
    .. code:: python
    
        edo12_constructors = [
            (sp.power.Pow(2,sp.Rational(2,12)), "T"),
            (sp.power.Pow(2,sp.Rational(1,12)), "s"),
        ]
        
    We can then create the standard major mode with:
    
    .. code:: python
    
        create_diatonic_scale(edo12_constructors, ["T","T","s","T","T","T","s"])
    
    which will yield:
    
    .. math::
    
        \\left [ 1, \\quad \\sqrt[6]{2}, \\quad \\sqrt[3]{2}, \\quad 2^{\\frac{5}{12}}, 
        \\quad 2^{\\frac{7}{12}}, \\quad 2^{\\frac{3}{4}}, \\quad 2^{\\frac{11}{12}}, 
        \\quad 2\\right ]
    
    
    '''
    scale = [sp.Integer(1)]
    count = 0
    if type(specification) == list:
        internal_spec = specification
    else:
        internal_spec = [x for x in specification]
    for interval in internal_spec:
        scale.append([x[0] * scale[count] for x in generators if x[1] == interval][0])
        count = count + 1
    return scale
    
