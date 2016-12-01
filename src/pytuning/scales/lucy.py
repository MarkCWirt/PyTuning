# -*- coding: utf-8 -*-
"""
Created on Tue May 26 13:56:12 2015

@author: mark
"""

# Note: The Lucy scale was used a lot in the initial implementation
# of PyTuning, because it was a bit complex and there was good documentation.
#
# However, I'm not personally too interested in the scale, so the work in this
# file is old and should be considered a bit suspect. The code probably works
# and is correct, but it has not been included in the unit tests, so it's
# accuracy (which was verified at the beginning) hasn't been checked for drift.

# I'm leaving this in the package for documentation, but again, consider this
# a bit suspect.

from __future__ import division, print_function

import sympy as sp
import numpy as np
import functools

from pytuning.scale_creation import find_factors, create_scale_from_scale
from pytuning.constants import lucy_construtors
from pytuning.utilities import normalize_interval
from pytuning.scales import create_diatonic_scale

def lucy_symbolic_to_simplified(input_spec):
    '''    
    Convert a symbolic representation of a Lucy scale degree to a simplified
    form.
    
    :param input_spec: The symbolic scale representation
    :returs: A simplified representation as a ``String``
    
    In general symbolic representations in ``pytuning`` look like the following:
    
    .. code::
    
        s1 = ['L','L','L','s']
        s2 = ['L','s','s']
        s3 = ['L','1/s','1/s']
        
    In simplified form:
    
    .. code::
    
        print(lucy_symbolic_to_simplified(s1))
        '3L+s'
        
        print(lucy_symbolic_to_simplified(s2))
        'L+2s'

        print(lucy_symbolic_to_simplified(s3))
        'L-2s'
    
    **Important Note** This particular function assumes that the input specification
    has been simplified for inversions and will not further simplify, thus we get:
    
    .. code::
    
        s = ['L','L','1/L','s','1/s','1/s']
        print(lucy_symbolic_to_simplified(s))
        '2L+s-L-2s'
        
    instead of the more simplified 'L-s'. However, most functions in the
    code (such as ``find_factors`` and things derived from this) will already
    have simplified the input, so this is not an issue. The simplification code
    may be incorporated into this function at a future date.
        
    '''
    lister = np.array(input_spec)
    number_L = np.sum(lister == 'L')
    number_s = np.sum(lister == 's')
    number_Li = np.sum(lister == '1/L')
    number_si = np.sum(lister == '1/s')
    output = ""
    if number_L != 0:
        output = output + str(number_L)+"L"
    if number_s != 0:
        if len(output) == 0:
            output = output + str(number_s)+"s"
        else:
             output = output + "+" + str(number_s)+"s"
    if number_Li != 0:
        output = output + "-" + str(number_Li)+"L"
    if number_si != 0:
        output = output + "-" + str(number_si)+"s"
    return output.replace("1L","L").replace("1s","s")

def create_lucy_tuning_spiral(scale_size=44, number_fourths=22, 
                              sort=False, octave=2):
    '''    
    Create the Lucy scale tuning spiral. The default values were chosen to
    match the published numbers
    
    :param scale_size: The number of intervals to produce
    :param number_fourth: The number of fourths to use
    :param sort: If True, the output will be sorted on scale size
    :param octave: The formal octave
    :returns: A list of tuples, the first member of which is the assigned symbol
        for the degree, and the second is the precise degree value (``sympy`` value).
    
    The tuning spiral is created by defining the Perfect Fifth and
    Perfect Fourth in terms of Lucy steps:
    
    .. math ::
    
        \\begin{align}
        P_5 & = L^3 \\cdot s \\cr
        P_4 &= L^2 \\cdot s
        \\end{align}
        
    The fourths and fifths are used as generators; in the default case, 22 of each are
    used to generate the target tones.
    
    **Important Note** According to the documentation of the scale, the fourths and
    fifths are taken in an opposite sense (which is to say one goes clockwise on the
    tuning circle, one goes counter-clockwise). However, based upon the published
    values *this is not really the case*. In this code both the fourths and the fifths
    are propagated in the same direction (no inversion is taken).
    
    The symbolic names are somewhat idiosyncratic and have been crafted by hand.
    '''
    L = sp.root(2,2*sp.pi)
    s = sp.sqrt(2/L**5)
    number_fifths   = scale_size - number_fourths
    r_5 = L*L*L*s
    r_4 = L*L*s
    
    output = []
    
    start = 1
    running_total = 1
    for index in range(number_fifths):
        scale_symbol =  ('#'*(running_total // 7))+str(start)
        x = r_5 ** index
        output = output + [(scale_symbol, normalize_interval(x, octave))]
        start = (start + 4) %7
        if start == 0:
            start = 7
        running_total = running_total + 1
        
    start = 1
    running_total = 1
    for index in range(number_fourths):
        scale_symbol = ('b'*((running_total+4) // 7))+str(start)
        x = (r_4) ** index
        output = output + [(scale_symbol, normalize_interval(x, octave))]
        start = (start + 3) %7
        if start == 0:
            start = 7
        if start == 1:
            start = 8
        running_total = running_total + 1
        
    output = output + [("8", sp.Integer(octave))]
    output =  list(output)
    if sort:
        output = sorted(set(output), key=lambda x: x[1])
    return output
    
def calculate_lucy_mode(mode):
    '''    
    Calculate a Lucy scale mode
    
    :param mode: The mode to calculate
    :returns: The mode, as a list of frequency ratios
    
The input mode should be a string with the intervals chosen from
the Lucy constructors, i.e. "L" and "s". As an example, 

.. code:: 

    calculate_lucy_mode("LLsL")
    
returns:

    .. math::
    
        \\left [ 1,  2^{\\frac{1}{2 \\pi}},  2^{\\frac{1}{\\pi}},  
        \\frac{\\sqrt{2}}{2^{\\frac{1}{4 \\pi}}},  
        \\sqrt{2} \\cdot 2^{\\frac{1}{4 \\pi}}\\right ]
        
A Lucy major scale could be calculated from:

.. code::

    calculate_lucy_mode("LLsLLLs")
    
and is numerically:

    .. math::
    
        \\left [ 1, 2^{\\frac{1}{2 \\pi}}, 2^{\\frac{1}{\\pi}}, 
        \\frac{\\sqrt{2}}{2^{\\frac{1}{4 \\pi}}}, \\sqrt{2} 
        \\cdot 2^{\\frac{1}{4 \\pi}}, \\sqrt{2} \\cdot 
        2^{\\frac{3}{4 \\pi}}, \\sqrt{2} \\cdot 2^{\\frac{5}{4 \\pi}}, 
        2\\right ]
~                                                                                                                
        
    '''
        
    split_mode = [x for x in mode]
    return create_diatonic_scale(lucy_construtors, split_mode)

def create_lucy_tone_table(scale_size=44, number_fourths=22, max_terms=8):
    '''
    .. py:function:: create_lucy_tone_table(scale_size=44, number_fourths=22, max_terms=8)
    
        Create a tone table for the Lucy scale
        
        :param scale_size: The number of degrees to generate
        :param number_fourth: The number of fourths to use in the tuning spiral
        :param max_terms: The maximum number of terms for tuning factorization
        :returns: A tone table (see below)
        
        This code works by creating a tuning spiral and then finding the factors which
        most closely them.
        
        The tone table is a list of tuples, with the members being:
        
        0. The symbolic name of the degree
        1. The symbolic factoring of the degree
        2. The precise value of the factored representation (``sympy`` value) 
        
        As an example, the first fre values from the defaults:
        
        .. code:: 

            [('1', [], 1),
             ('5', ['L', 'L', 'L', 's'], sqrt(2)*2**(1/(4*pi))),
             ('2', ['L'], 2**(1/(2*pi))),
             ('6', ['L', 'L', 'L', 'L', 's'], sqrt(2)*2**(3/(4*pi))),
             ('3', ['L', 'L'], 2**(1/pi)), ...]
             
        The tone table can be passed to ``find_factors`` to create a constrained
        finding routine.
    '''
    lucy_tuning_spiral = create_lucy_tuning_spiral(scale_size=scale_size, number_fourths=number_fourths)
    lucy_scale = []
    for degree in lucy_tuning_spiral:
        lucy_scale = lucy_scale + [find_lucy_interval(degree[1],max_terms=max_terms)]
    return [(lucy_tuning_spiral[i][0],
            lucy_scale[i][1], 
            lucy_scale[i][2]) for i in range(len(lucy_tuning_spiral))]
    
def calculate_lucy_mode_twelve_tone(mode):
    '''    
    Calculate a diatonic mode for the Lucy Scale
    
    :param: The mode to calculate
    :returns: the mode
    
    This is a convenience function to take a mode definition and
    create a 12-tone equivalent. It does it by placing relatively
    arbitrary values in the non-mode positions. The main use for this
    would be to create a synthesizer tuning table. Notes outside the
    mode should not be played.
    
    The entries in the mode string should be "L" or "s", for the long
    and sort step respectively.
    
    As an example, the major mode in the lucy scale:
    
    .. code::
    
        scale = calculate_lucy_mode_twelve_tone('LLsLLLs')

    yields:
    
    .. math::
    
        \\left [ 1, 1, \2^{\\frac{1}{2 \\pi}}, 1, 2^{\\frac{1}{\\pi}}, 
        \\frac{\\sqrt{2}}{2^{\\frac{1}{4 \\pi}}}, 1, \\sqrt{2} 
        \\cdot 2^{\\frac{1}{4 \\pi}}, 1, \\sqrt{2} \\cdot 2^{\\frac{3}{4 \\pi}}, 1, 
        \\sqrt{2} \\cdot 2^{\\frac{5}{4 \\pi}}, 2 \\right ]
        
    Note that 1 is assigned to the non-mode positions.

    '''
    scale = calculate_lucy_mode(mode)
    output = [sp.Integer(1)]
    for index in range(len(mode)):
        if mode[index] == 'L':
            output = output + [sp.Integer(1)] + [scale[index+1]]
        else:
            output = output + [scale[index+1]]
    return output
    
# Derived Functions
    
find_lucy_interval = functools.partial(
    find_factors, constructors=lucy_construtors,
    max_terms=15)
                                        
def create_lucy_scale_from_scale(scale, max_terms=8, tone_table=None):
    '''    
    Given a target scale, calculate the closest matching Lucy scale.
    
    :param scale: The target scale (list or ratios)
    :param max_terms: The maximum number of terms for the factoring
        along the basis intervals
    :param tone_table: A constrained tone table (see below)
    :returns: A tuple, the first member of which is a list
        of the derived scale values, and the second of which is
        a symbolic representation of the factoring found.
    
    
    
    As an example of use, if we were to try to match
    a Pythagorean scale with an unconstrained factoring of the
    Lucy intervals (i.e., with no tone table):
    
    .. code::
    
        pythag = create_pythagorean_scale()
        lp = create_lucy_scale_from_scale(pythag)
        
    yields
    
    .. code::
    
        ([1,
          (64*sqrt(2))**(1/pi)/4,
          sqrt(2)*(32*2**(1/4))**(1/pi)/4,
          4*(sqrt(2)/64)**(1/pi),
          sqrt(2)*(32*2**(3/4))**(1/pi)/4,
          2**(-1/(4*pi) + 1/2),
          sqrt(2)*(64*2**(1/4))**(1/pi)/4,
          2**(1/(4*pi) + 1/2),
          4*sqrt(2)*(2**(1/4)/64)**(1/pi),
          (32*sqrt(2))**(1/pi)/2,
          4*sqrt(2)*(2**(3/4)/64)**(1/pi),
          8*(sqrt(2)/128)**(1/pi),
          2],
         [[],
          ['1/s', '1/s', '1/s', '1/s', 'L', 'L', 'L'],
          ['1/s', '1/s', '1/s', 'L', 'L', 'L'],
          ['1/L', 's', 's', 's', 's'],
          ['1/s', '1/s', '1/s', 'L', 'L', 'L', 'L'],
          ['L', 'L', 's'],
          ['1/s', '1/s', '1/s', 'L', 'L', 'L', 'L', 'L'],
          ['L', 'L', 'L', 's'],
          ['L', 's', 's', 's', 's', 's'],
          ['1/s', '1/s', 'L', 'L', 'L', 'L', 'L', 'L'],
          ['L', 'L', 's', 's', 's', 's', 's'],
          ['L', 'L', 's', 's', 's', 's', 's', 's'],
          ['L', 'L', 'L', 'L', 'L', 's', 's']])

    '''
    return  create_scale_from_scale(scale=scale, 
                                    interval_function=find_lucy_interval, 
                                    max_terms=max_terms, 
                                    tone_table=tone_table)

                                        
if __name__ == '__main__':
    from pytuning.scales import create_harmonic_scale
    from pytuning.utilities import compare_two_scales
    scale = create_harmonic_scale(8,32)
    lucy_scale = create_lucy_scale_from_scale(scale)
    compare_two_scales(scale, lucy_scale[0], title=["Harmonic", "Lucy Unconstrained"])
    
