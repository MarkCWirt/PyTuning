# -*- coding: utf-8 -*-
"""
Created on Tue May 26 11:46:12 2015

@author: mark
"""

import sympy as sp
import itertools
import operator

from pytuning.utilities import normalize_interval

# Moved in Python 3
try:
    import functools
    reduce = functools.reduce
except:
    pass

def create_euler_fokker_scale(intervals, multiplicities, octave=2, normalize=True):
    '''    
    Create a scale in the Euler-Fokker Genera
    
    :param intervals: The factors to use for the construction (usually prime
        numbers)
    :param multiplicities: The multiplicities of the factors (see below)
    :param octave: The formal octave
    :param normalize: If ``True``, normalize the intervals to the octave.
    
    ``intervals`` and ``multiplicities`` should both be lists of equal length.
    The entries in ``multiplicities`` give the number of each factor to use.
    Therefore the following:
    
    .. code::
    
        intervals     = [3,5,7]
        multiplicities = [1,1,1]
        scale         = create_euler_fokker_scale(intervals, multiplicities)
        
    Will create a scale with one 3, one 5, and one 7 as generators.
    
    The above will produce the following scale:
    
    .. math::
    
        \\left [ 1, \\frac{35}{32}, \\frac{5}{4}, \\frac{21}{16}, \\frac{3}{2}, \\frac{105}{64}, 
        \\frac{7}{4}, \\frac{15}{8}, 2\\right ]
        
    Also note that the two statements will generate the same output:
    
    .. code::
    
        intervals     = [3,5,7]
        multiplicities = [2,2,1]
        scale1        = create_euler_fokker_scale(intervals, multiplicities)

        intervals     = [3,3,5,5,7]
        multiplicities = [1,1,1,1,1]
        scale2        = create_euler_fokker_scale(intervals, multiplicities)
        
        scale1 == scale2
        True
    '''

    output = []
    for index in range(len(intervals)):
        output = output + [intervals[index]] * multiplicities[index]
        output = [sp.Integer(x) for x in output]
        
    potential = list(itertools.chain(*[[x for x in itertools.combinations(output,r)] 
                                       for r in range(1,len(output)+1)]))
    output = []
    for item in potential:
        if len(item) == 0:
            output = output + [item[0]]
        else:
            output = output + [reduce(operator.__mul__, item)]


    if normalize:
        output = [sp.Integer(1)] + [normalize_interval(x, octave) for x in output] + [sp.Integer(octave)]
    else:
        output = [sp.Integer(1)] + [x for x in output] + [sp.Integer(octave)]

    output = sorted(set(output))
    return output
