# -*- coding: utf-8 -*-
"""
Created on Tue May 26 11:01:24 2015

@author: mark
"""
from __future__ import print_function, division

import sympy as sp
from pytuning.utilities import normalize_interval

def create_harmonic_scale(first_harmonic, last_harmonic, normalize=True, octave=2):
    '''    
    Create a harmonic scale
    
    :param first_harmonic: The first harmonic
    :param last_harmonic: The last harmonic
    :param normalize: If true, normalize the scale to an octave 
                      (2/1 by default, otherwise taken from ``octave``)
    :param octave: The definition of the formal octave.
    :returns: The scale
    
    As an example of use, a normalized scale constructed from harmonics
    3 to 20:
    
    .. code::
    
        scale = create_harmonic_scale(3,20)
        
    which yields:
    
    .. math::
    
        \\left [ 1, \\frac{13}{12}, \\frac{7}{6}, \\frac{5}{4}, \\frac{4}{3}, 
        \\frac{17}{12}, \\frac{3}{2}, \\frac{19}{12}, \\frac{5}{3}, \\frac{11}{6}, 2\\right ]
        
    To create a non-normalized scale:
    
    .. code::
    
        scale = create_harmonic_scale(3,10, normalize=False)
        
    which yields:
    
    .. math:: 
    
        \\left [ 1, \\frac{4}{3}, \\frac{5}{3}, 2, \\frac{7}{3}, \\frac{8}{3}, 3, 
        \\frac{10}{3}\\right ]
    '''
    r = [sp.Integer(1) + sp.Integer(1)*(i) for i in range(last_harmonic)]
    r = r[first_harmonic-1:]
    r = [i / r[0] for i in r]
    output = []
    for interval in r:
        if normalize:
            interval = normalize_interval(interval, octave)
        output = output + [interval]
    output = sorted(list(set(output)))
    
    if normalize:
        output = [sp.Integer(1)] + [normalize_interval(x, octave) for x in output] + [sp.Integer(octave)]
    else:
        output = [sp.Integer(1)] + [x for x in output] + [sp.Integer(octave)]
    
    output = sorted(set(output))
    
    return output
