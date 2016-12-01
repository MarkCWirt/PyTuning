# -*- coding: utf-8 -*-
"""
Created on Tue May 26 11:42:12 2015

@author: mark
"""


import sympy as sp

def create_edo_scale(number_tones, octave=2):
    '''    
    Create an equal division of octave (EDO, ET) scale.
    
    :param number_tones: The number of tones/divisions in the scale
    :param octave: The formal octave (frequency ratio)
    
    Example, 12T-ET:
    
    .. code:: python
    
        edo_scale = create_edo_scale(12)
        
    will yield the normal equal-tempered scale used in western music:
    
    .. math::
    
        \\left [ 1, \\sqrt[12]{2}, \\sqrt[6]{2}, \\sqrt[4]{2}, \\sqrt[3]{2}, 2^{\\frac{5}{12}}, 
        \\sqrt{2}, 2^{\\frac{7}{12}}, 2^{\\frac{2}{3}}, 2^{\\frac{3}{4}}, 2^{\\frac{5}{6}}, 
        2^{\\frac{11}{12}}, 2\\right ]
        
    Note that the length of the scale is 13, as both the unison and octave are
    included by convention.
    
    It is also possible to have a non-2 formal octave. The code:
    
    .. code:: python
    
        edo_scale = create_edo_scale(12,3)
        
    will yield:
    
    .. math::
    
        \\left [ 1, \\sqrt[12]{3}, \\sqrt[6]{3}, \\sqrt[4]{3}, \\sqrt[3]{3}, 3^{\\frac{5}{12}}, 
        \\sqrt{3}, 3^{\\frac{7}{12}}, 3^{\\frac{2}{3}}, 3^{\\frac{3}{4}}, 3^{\\frac{5}{6}}, 
        3^{\\frac{11}{12}}, 3\\right ]
    '''
    division      = sp.Integer(octave)**sp.Rational(1,number_tones)
    output = []
    for index in range(number_tones+1):
        output = output + [division**index]
    return output
