# -*- coding: utf-8 -*-
"""
Created on Tue May 26 11:36:57 2015

@author: mark
"""
from __future__ import print_function, division

from pytuning.scales.equal_interval import create_equal_interval_scale
from pytuning.constants import perfect_fifth


def create_pythagorean_scale(scale_size=12, number_down_fifths=6, 
                          epsilon=None, sort=True, octave=2, remove_duplicates=True):
    '''    
    Create a Pythagorean scale
    
    :param scale_size: The number of degrees in the scale
    :param number_down_fifths: The number of inverted fifths to use in
        scale construction.
    :param epsilon: Rounding parameter. If set to ``None`` no rounding is
        done. Otherwise the scale degrees are rounded to the nearest
        epsilon
    :param sort: If ``True``, sort the output by degree size
    :param octave: The formal octave
    :param remove_duplicates: If ``True`` remove duplicate entries
    
    The Pythagorean scale is an even-interval scale with the
    following generating interval:
    
    .. math::
        
            P_5 = \\frac{3}{2}
    '''
                              
    return create_equal_interval_scale(perfect_fifth, 
                                       scale_size=scale_size, 
                                       number_down_intervals=number_down_fifths, 
                                       epsilon=epsilon, 
                                       sort=sort, octave=octave, 
                                       remove_duplicates=remove_duplicates)
