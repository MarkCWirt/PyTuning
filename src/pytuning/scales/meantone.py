# -*- coding: utf-8 -*-
"""
Created on Tue May 26 13:23:32 2015

@author: mark
"""
from __future__ import print_function, division

from pytuning.constants import perfect_fifth, quarter_comma
from pytuning.scales.equal_interval import create_equal_interval_scale

import sympy as sp

quarter_comma_meantone_fifth = perfect_fifth / quarter_comma


def create_quarter_comma_meantone_scale(scale_size=12, number_down_fifths=6, 
                          epsilon=None, sort=True, octave=2, remove_duplicates=True):
    '''
    
    Create a quarter-comma meantone scale
    
    :param scale_size: The number of degrees in the scale
    :param number_down_fifths: The number of inverted fifths to use in
        scale construction.
    :param epsilon: Rounding parameter. If set to ``None`` no rounding is
        done. Otherwise the scale degrees are rounded to the nearest
        epsilon
    :param sort: If ``True``, sort the output by degree size
    :param octave: The formal octave
    :param remove_duplicates: If ``True`` remove duplicate entries
    
    The quarter-comma meantone scale is an even-interval scale with the
    following generating interval:
    
    .. math::
        
            P_5 = \\frac{\\frac{3}{2}}{\\sqrt[4]{\\frac{81}{80}}}
            
    which is a perfect fifth (in a Pythagorean sense) narrowed by
    one quarter of the syntonic comma.
        
        
    '''
                              
    return create_equal_interval_scale(quarter_comma_meantone_fifth, 
                                 scale_size=scale_size, 
                                 number_down_intervals=number_down_fifths, 
                                 epsilon=epsilon, 
                                 sort=sort, octave=octave, 
                                 remove_duplicates=remove_duplicates)
    
def convert_p5_to_r(p5):
    '''
    .. py:function:: convert_p5_to_r(p5)
    
        Convert a meantone generating interval to an **R** value
        
        :param p5: The generating interval
        :returns: the R value for the interval
    '''
    log_p5 = sp.log(p5)/sp.log(2)
    R = (1-2*log_p5)/(5*log_p5-3)
    return R
    
def convert_r_to_p5(r):
    '''
    .. py:function:: convert_r_to_p5(r)
    
        Convert an **R** value to a meantone generating interval
        
        :param r: The R value
        :returns: The generating interval
    '''
    p5 = 2**((3*r+1)/(5*r+2))
    return p5
