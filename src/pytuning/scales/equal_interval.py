# -*- coding: utf-8 -*-
"""
Created on Tue May 26 11:57:03 2015

@author: mark
"""

from __future__ import print_function, division
import sympy as sp
from pytuning.utilities import normalize_interval

def create_equal_interval_scale(generator_interval, scale_size=12, number_down_intervals=6, 
                          epsilon=None, sort=True, octave=2, remove_duplicates=True, 
                          normalize=True):
    '''    
    Create a scale with equal-interval tuning
    
    :param generator_interval: The interval to use for generation (``sympy`` value)
    :param scale_size: The number of degrees in the scale
    :param number_down_intervals: The number of inverted intervals to use in
        scale construction.
    :param epsilon: Rounding parameter. If set to ``None`` no rounding is
        done. Otherwise the scale degrees are rounded to the nearest
        epsilon
    :param sort: If ``True``, sort the output by degree size
    :param octave: The formal octave
    :param remove_duplicates: If ``True`` remove duplicate entries
    :param normalize: IF ``True``, normalize the degrees to the octave
    
    In general one should keep epsilon at ``None`` and perform and
    rounding outside the function.
    
    This is a base function from which several other scales are derived,
    including:
    
    * The Pythagorean scale
        A scale with a perfect
        fifth (3/2) as the generating interval
        
        .. math::
        
            P_5 = \\frac{3}{2}
            
    * The quarter-comma meantone scale
        A scale in which the generating
        interval is a perfect fifth narrowed by one quarter of syntonic
        comma
        
        .. math::
        
            P_5 = \\frac{\\frac{3}{2}}{\\sqrt[4]{\\frac{81}{80}}}
            
    * EDO Scales
        EDO scales can be generated from an appropriate selection of the
        fifth. For example, the 12-TET scale would use the fifth:
        
        .. math::
        
            P_5 = \\sqrt[\\frac{7}{12}]{2}
    '''
    down_intervals = number_down_intervals + 1
    up_intervals   = scale_size - down_intervals + 1
    r_5 = generator_interval
    output = []
    for index in range(up_intervals):
        x = r_5 ** index
        if normalize:
            output = output + [normalize_interval(x, octave)]
        else:
            output = output + [x]
    for index in range(down_intervals):
        x = (1/r_5) ** index
        if normalize:
            output = output + [normalize_interval(x, octave)]
        else:
            output = output + [x]
    output = output + [sp.Integer(octave)]
    if epsilon is not None:
        output =  list(set([round(y/epsilon)* epsilon for y in output]))
    else:
        output =  list(output)
    if sort:
        output = sorted(output)
        if remove_duplicates:
            output = sorted(set(output))
    return output
