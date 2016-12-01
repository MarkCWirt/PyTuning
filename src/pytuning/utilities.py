# -*- coding: utf-8 -*-
"""
Created on Tue May 26 10:36:08 2015

@author: mark
"""

from __future__ import print_function, division
import sympy as sp
import itertools

import pytuning.constants

__all__ = ["normalize_interval", "distinct_intervals", "get_mode_masks", "mask_scale", "mask_to_steps", \
           "ratio_to_cents", "cents_to_ratio", "note_number_to_freq", "compare_two_scales",
           "ratio_to_name"]

def normalize_interval(interval, octave=2):
    '''
    
    Normalize a musical interval
    
    :param interval: The interval to normalize. Should be a frequency
                     ratio, most usefully expressed as a `sympy.Rational`
                     or related data item
    :param octave: The formal octave. Defaults to 2
    :returns: The interval, normalized
    
    Note that any formal octave can be used. In normal usage a
    2 will be used (i.e., a doubling of frequency is an octave).
    
    Normalization works by finding the smallest power of two (or ``octave``) that when multiplied
    by the interval (in the case of an interval less than 1) or divided into
    the interval (for intervals greater than 2) will bring the interval into
    the target range of :math:`1 \\le i \\le 2`.
    '''
    if interval >= octave:
        return interval/(octave**(sp.ceiling((sp.log(interval/octave)/sp.log(octave)).evalf())))
    elif interval < 1:
        return interval*(octave**(sp.floor((sp.log(octave/interval)/sp.log(octave)).evalf())))
    else:
        return interval

def distinct_intervals(scale):
    '''    
    Find the distinct intervals in a scale, including inversions
    
    :param scale: The scale to analyze
    :returns: A list of distinct intervals
    
    The scale should be specified as a list of ``sympy`` numerical
    values (``Rational`` or ``Integer``). Note that the convention adopted
    in this code is that scale[0] is a unison and scale[-1] is
    the formal octave (often 2).
    
    As an example of a valid scale, a standardized Pythagorean
    tuning could be passed into the function:
    
    .. math:: 
    
        \\left [ 1, \\frac{256}{243}, \\frac{9}{8}, \\frac{32}{27}, 
        \\frac{81}{64}, \\frac{4}{3}, \\frac{1024}{729}, \\frac{3}{2}, 
        \\frac{128}{81}, \\frac{27}{16}, \\frac{16}{9}, 
        \\frac{243}{128}, 2\\right ]
        
    If one were hand-crafting this scale, it would look something like:
    
    .. code::
    
        import sympy as sp
        scale = [sp.Integer(1), sp.Rational(256,243), sp.Rational(9,8), ...]
        
    The function returns a list in rational/symbolic terms. If numerical
    values are needed, one can, for example, map ``ratio_to_cents`` to
    obtain it:
    
    .. code::
    
        di = distinct_intervals(scale)
        di_in_cents = [ratio_to_cents(x) for x in di]
            
    '''
    base = scale[-1] # the formal octave
    # Make the scale span two octaves to get inversions
    temp_scale = scale + [x*sp.Integer(base) for x in scale]
    pairs = [x for x in itertools.combinations(temp_scale,2)]
    #intervals = sorted(list(set(map(lambda x: x[1]/x[0], pairs))))
    intervals = list(set(map(lambda x: x[1]/x[0], pairs)))
    intervals = filter (lambda x: x < 2, intervals)
    intervals = filter (lambda x: x != 1, intervals)
    return [x for x in intervals]

def get_mode_masks(total_tones, selected_tones):
    '''    
    Get all potential mode masks
    
    :param total_tones: The total number of degrees in the scale
    :param selected_tones: The number of degrees in the mode
    :returns: A list of mode masks
    
    A mode mask selects tones from a chromatic scale and returns
    the notes selected for the mode. This function returns all
    of the potential mode masks for a given combination of
    ``total_tones`` and ``selected_tones``. Each mask it a 
    zero-origined tuple of the notes in the mode. It also includes
    the unison and formal octave.
    
    As an example, to find all the potential three-note modes
    in a seven note scale one would call:
    
    .. code::
    
        get_mode_masks(7,3)
        
    the results of which would be:
    
    .. code::
    
        [(0, 1, 6), (0, 2, 6), (0, 3, 6), (0, 4, 6), (0, 5, 6)]
    
    
    Note that 0 and 6 (the unison and octave) are returned in
    each potential mode.
    '''
    masks =  [y for y in itertools.combinations([x for x in range(total_tones)],
                                                 selected_tones)]
    # Make sure the unison/octave is in the mode
    masks = filter(lambda x: 0 in x and total_tones-1 in x, masks)
    # Python 2 vs 3. In three the filter function doesn't return a list, so
    # we'll so that here. For python 2 this is basically a null operation
    return [x for x in masks]

def mask_scale(scale, mask):
    '''    
    Apply a mode mask to a scale
    
    :param scale: The scale to analyze (a list of frequency
        ratios)
    :param mask: The mode mask
    
    As an example of use, assuming that we have a
    standard Pythagorean scale, i.e:
    
    .. math::

        \\left [ 1, \\frac{256}{243}, \\frac{9}{8}, \\frac{32}{27}, 
        \\frac{81}{64}, \\frac{4}{3}, \\frac{1024}{729}, \\frac{3}{2}, 
        \\frac{128}{81}, \\frac{27}{16}, \\frac{16}{9}, 
        \\frac{243}{128}, 2\\right ]
        
    We could use the following to create a diatonic major scale:
    
    .. code::
    
        pythag = create_pythagorean_scale()
        mask = (0,2,4,5,7,9,11,12)
        mode_scale = mask_scale(pythag, mask)
        
    which would yield:
    
    .. math::
    
        \\left [ 1, \\frac{9}{8}, \\frac{81}{64}, \\frac{4}{3}, 
        \\frac{3}{2}, \\frac{27}{16}, \\frac{243}{128}, 2\\right ]
    '''
    return [x for x in filter (lambda a: a is not None, [scale[i] if i in mask 
                            else None for i in range(len(scale))])]

def mask_to_steps(scale, mask):
    '''    
    Convert a mode mask to step format.
    
    :param scale: The scale at hand (ratio of frequencies)
    :param mask: The mode mask
    :returns: The mode mask in step format
    
    Note that scale is needed so that the total length of the
    scale is known, but otherwise isn't used. If a scale isn't
    really needed one could just pass in something like:
    
    .. code::
    
        [0]*13
        
    As an example of use:
    
    .. code::
    
        pythag = create_pythagorean_scale()
        mask = (0,2,4,5,7,9,11,12)
        steps = mask_to_steps(pythag, mask)
        
    which yields:
    
    .. code::
    
        [2, 2, 1, 2, 2, 2, 1]
        
    which is the major mode.
    '''
    steps = [mask[x] - mask[x-1] for x in range(1,len(mask))]
    if len(scale)- sum(steps) -1 != 0:
        steps = steps + [len(scale)- sum(steps) -1]
    return steps

def ratio_to_cents(ratio):
    '''    
    Convert a scale degree to a cent value
    
    :param ratio: The scale degree (``sympy`` value)
    :returns: The scale degree in cents
    
    Calculates:
    
    .. math::
    
        \\sqrt[2^{\\left[ \\frac{1}{1200} \\right]}]{\\text{degree}}

    Note that this function returns a floating point number,
    not a ``sympy`` ratio.
    '''
    cent = sp.Integer(2) ** sp.Rational(1,1200)
    return (sp.log(ratio)/sp.log(cent)).evalf()

def cents_to_ratio(cents):
    '''    
    Convert a cent value to a ratio
    
    :param cents: The degree value in cents
    :returns: the frequency ratio
    
    '''
    cent = sp.Integer(2) ** sp.Rational(1,1200)
    return sp.exp(cents * sp.log(cent)).evalf()

def note_number_to_freq(note, scale = None, reference_note=69, 
                        reference_frequency=440.0):
    '''                        
    Convert a note number (MIDI) to a frequency (Hz).
    
    :param note: The note number (0<=note<=127)
    :param scale: The scale. If none it assume EDO 12.
    :param reference note: The conversions reference note
    :param reference_frequency: The frequency of the reference note
    :returns: The frequency of the note in Hertz
    
    The default values for ``reference_note`` and
    ``reference_frequency`` correspond to standard
    orchestral tuning, a4 = 440 Hz.
    '''
    if scale is None:
        scale = scale = [(sp.Integer(2)**sp.Rational(1,12))**index for index in range(13)]
    octave_offset = (note - reference_note) // (len(scale)-1)
    note_offset   = (note - reference_note) %  (len(scale)-1)
    base = scale[-1].evalf()
    octave_multiplier = base ** abs(octave_offset)
    if octave_offset < 0:
        octave_multiplier = 1.0/ octave_multiplier
    freq = (reference_frequency * octave_multiplier) * scale[note_offset]
    return freq.evalf()

def compare_two_scales(scale1, scale2, reference_freq=220.0, 
                       title=["Scale1", "Scale2"]):
    '''    
    Compare two scales
                       
        :param scale1: The first scale (list of ``sympy`` values)
        :param scale2: The second scale (list of ``sympy`` values)
        :param reference_freq: The frequency (Hz) of the first degree
        :param title: The scale names (list of strings with len = 2)
        :returns: ``None``, (ie nothing)
    '''
    print( "%21s %21s" % (title[0], title[1]))
    print( "     Cents       Freq      Cents       Freq  Delta(Cents)")
    print( " =========  =========  =========  =========  ============")
    for index in range(len(scale1)):
        print( "%10.4f %10.4f %10.4f %10.4f    %10.4f" % (
            ratio_to_cents(scale1[index]), 
            (scale1[index]*reference_freq).evalf(), 
            ratio_to_cents(scale2[index]), 
            (scale2[index]*reference_freq).evalf(),
            ratio_to_cents(scale1[index]) - ratio_to_cents(scale2[index])
            ))
        
def ratio_to_name(ratio):
    '''
    Convert a scale degree to a name
    
    :param ratio: The input scale degree (a ``sympy`` value)
    :returns: The degree name if found, ``None`` otherwise
    '''
    entries = [x[0] for x in pytuning.constants.interval_catalog if x[1] == ratio]
    if len(entries) == 0:
        return None
    else:
        return entries[0]
