# -*- coding: utf-8 -*-
"""
Created on Tue May 26 11:11:58 2015

@author: mark
"""
from __future__ import print_function, division

import sympy as sp
import numpy as np
import itertools
import operator

# Moved in Python 3
try:
    import functools
    reduce = functools.reduce
except:
    pass

from pytuning.utilities import get_mode_masks, mask_scale, mask_to_steps
from pytuning.metrics import all_metrics

def calculate_modes(scale, num_tones, metric_function=None):
    '''    
    Calculate all possible modes for a scale
    
    :param scale: The scale to analyze
    :param num_tones: The number of tones for the scale. Note that the
        actual scale has one additional tone, as the convention in this
        package is to include both the unison and the formal octave
    :param metric_function: The metric function to use. 
        If unspecified all defined metrics (from ``pytuning.metrics``)
        will be used.
        
    As an example, we can find all 7-note modes of the
    Pythagorean scale with the following:
    
    .. code::
    
        pythag = create_pythagorean_scale()
        modes = calculate_modes(pythag, 7)
        
    will produce a total of 462 modes, the first
    three of which are:
    
    .. code:: 
    
        [{'mask': (0, 1, 2, 3, 4, 5, 6, 12),
          'metric_3': 42.3282000153386,
          'original_scale': [1,
           256/243,
           9/8,
           32/27,
           81/64,
           4/3,
           1024/729,
           3/2,
           128/81,
           27/16,
           16/9,
           243/128,
           2],
          'scale': [1, 256/243, 9/8, 32/27, 81/64, 4/3, 1024/729, 2],
          'steps': [1, 1, 1, 1, 1, 1, 6],
          'sum_distinct_intervals': 20,
          'sum_p_q': 2485,
          'sum_p_q_for_all_intervals': 345222,
          'sum_q_for_all_intervals': 144598},
         {'mask': (0, 1, 2, 3, 4, 5, 7, 12),
          'metric_3': 41.8570135746606,
          'original_scale': [1,
           256/243,
           9/8,
           32/27,
           81/64,
           4/3,
           1024/729,
           3/2,
           128/81,
           27/16,
           16/9,
           243/128,
           2],
          'scale': [1, 256/243, 9/8, 32/27, 81/64, 4/3, 3/2, 2],
          'steps': [1, 1, 1, 1, 1, 2, 5],
          'sum_distinct_intervals': 16,
          'sum_p_q': 737,
          'sum_p_q_for_all_intervals': 103410,
          'sum_q_for_all_intervals': 42124},
         {'mask': (0, 1, 2, 3, 4, 5, 8, 12),
          'metric_3': 41.5804178299798,
          'original_scale': [1,
           256/243,
           9/8,
           32/27,
           81/64,
           4/3,
           1024/729,
           3/2,
           128/81,
           27/16,
           16/9,
           243/128,
           2],
          'scale': [1, 256/243, 9/8, 32/27, 81/64, 4/3, 128/81, 2],
          'steps': [1, 1, 1, 1, 1, 3, 4],
          'sum_distinct_intervals': 18,
          'sum_p_q': 941,
          'sum_p_q_for_all_intervals': 128820,
          'sum_q_for_all_intervals': 52781}]
        
    The meaning of the keys are as follows:
    
    * m1-m4: 
        A metric value. Note that if you apply
        your own metric function it should return a one-element
        ``dict`` with the metric name as the key. The return of
        this function can include multiple metrics (as does
        the default ``all_metrics`` function).
    * mask: 
        The mode mask (the degrees in the mode). Note that
        this is zero-origined and will by default only include
        modes with include the unison/octave, where the formal
        octave is given by the last degree of the input scale.
    * scale: 
        The scale for the mode.
    * steps: 
        The step representation of the mask.
    '''
    masks = get_mode_masks(len(scale),num_tones+1)
    output = []
    for mask in masks:
        temp_scale = mask_scale(scale, mask)
        if metric_function is not None:
            metrics = metric_function(temp_scale)
        else:
            metrics = all_metrics(temp_scale)
        output = output + [
            {
                "scale"          : temp_scale,
                "mask"           : mask,
                "steps"          : mask_to_steps(scale,mask),
                "original_scale" : scale,
            }
        ]
        for key in metrics:
            output[-1][key] = metrics[key]
    return output

def find_best_modes(scale, num_tones, 
                    sort_order=['sum_p_q_for_all_intervals','sum_p_q','sum_distinct_intervals'], 
                    num_scales=1, metric_function=None):
    '''
    Find the best modes for a scale, as defined by the specified
    metrics.
    
    :param scale: The scale to analyze
    :param num_tones: The number of degrees in the mode
    :param sort_order: How the return should be sorted, referenced
        to the metrics calculated
    :param num_scales: The number of scales to return. If ``None``
        all scales will be returned
    :param metric_function: The metric function to use. If
        ``None`` then ``all_metrics`` will be used.
    :returns: A sorted list of mode objects.
        
    The sort order is a list of keys that the metric function
    should return, applied in order, with an assumption that
    the lower the metric the more consonant (and "better") the
    scale. As an example, the default sort order:
    
    .. code::
    
        ['sum_p_q_for_all_intervals','sum_p_q','sum_distinct_intervals']
        
    Will order the scales by increasing **sum_p_q_for_all_intervals**. If two scales
    have the same **sum_p_q** value they will be secondarily sorted
    on **sum_p_q**. If scales have the same **sum_p_q_for_all_intervals** and **sum_p_q** then
    **sum_distinct_intervals** will be used.
    
    If no metric function is specified the default ``all_metrics``
    will be used. However, for efficiency one may not want to
    calculate all metrics if they are not being used. For example,
    if one is just interested in one metric, you can pass the metric
    directly:
    
    .. code:: python
    
        from pytuning import create_pythagorean_scale
        from pytuning.metrics import sum_p_q_for_all_intervals
        
        pythag = create_pythagorean_scale()
        my_metric = lambda scale: dict(sum_p_q(scale), **sum_p_q_for_all_intervals(scale))
        
        best_modes = find_best_modes(pythag, 7, sort_order=['sum_p_q_for_all_intervals'],
                        num_scales=1, metric_function=sum_p_q_for_all_intervals)
                        
    which would yield:
    
    .. code:: python
    
        [{'mask': (0, 1, 3, 5, 6, 8, 10, 12),
          'original_scale': [1,
           256/243,
           9/8,
           32/27,
           81/64,
           4/3,
           1024/729,
           3/2,
           128/81,
           27/16,
           16/9,
           243/128,
           2],
          'scale': [1, 256/243, 32/27, 4/3, 1024/729, 128/81, 16/9, 2],
          'steps': [1, 2, 2, 1, 2, 2, 2],
          'sum_p_q_for_all_intervals': 4374}]
    
    If one is interested in two of the metrics, you could, for example:
        
    .. code:: python
    
        from pytuning import create_pythagorean_scale
        from pytuning.metrics import sum_p_q, sum_p_q_for_all_intervals
        
        pythag = create_pythagorean_scale()
        my_metric = lambda scale: dict(sum_p_q(scale), **sum_p_q_for_all_intervals(scale))
        
        best_modes = find_best_modes(pythag, 7, sort_order=['sum_p_q','sum_p_q_for_all_intervals'],
                        num_scales=1, metric_function=my_metric)
        
    
    which would yield:
        
    .. code:: python
    
        [{'mask': (0, 2, 3, 5, 7, 9, 10, 12),
          'original_scale': [1,
           256/243,
           9/8,
           32/27,
           81/64,
           4/3,
           1024/729,
           3/2,
           128/81,
           27/16,
           16/9,
           243/128,
           2],
          'scale': [1, 9/8, 32/27, 4/3, 3/2, 27/16, 16/9, 2],
          'steps': [2, 1, 2, 2, 2, 1, 2],
          'sum_p_q': 161,
          'sum_p_q_for_all_intervals': 4374}]
    '''
    
    if metric_function is not None:
        scales = calculate_modes(scale, num_tones, 
                                  metric_function=metric_function)
    else:
        scales = calculate_modes(scale, num_tones)
    scales = sorted(scales, key=lambda x: tuple(
            x[y] for y in sort_order)
            )
    if num_scales is not None:
        return scales[:num_scales]
    else:
        return scales
    
def find_factors(interval, constructors, max_terms=8):
    '''    
        Factor an interval over a given set of basis generators,
        finding the best match
        
        :param interval: The interval to match (``sympy`` value)
        :param constructors: The generator functions (see below)
        :param max_terms: The maximum number of factors to return
        :returns: A list that contains a breakdown of the interval
            in terms of the basis intervals, a symbolic representation
            of the same, and the total precise interval represented
            my this breakdown.
            
        The constructors are given as a list of tuples, the first
        value being the numerical value of the generator function
        and the second being a single-character symbolic representation
        of that interval. There are several constructor sets
        defined in ``pytuning.constants`` an example of which is
        the 12-EDO constructor:
        
        .. code::
        
            edo12_constructors = [
                (sp.power.Pow(2,sp.Rational(2,12)), "T"), # a tone
                (sp.power.Pow(2,sp.Rational(1,12)), "s"), # a semi-tone
            ]
            
        If, for example, we wanted to try to match a perfect
        (Pythagorean) fifth to a 12-EDO tuning:
        
        .. code::
        
            p5 = sp.Rational(3,2)
            edo_rep = find_factors(p5, edo12_constructors)
            
        returns
        
        .. code::
        
            ([2**(1/6), 2**(1/6), 2**(1/6), 2**(1/12)], ['T', 'T', 'T', 's'], 2**(7/12))
        
        
        In this case the actual value of the return:
        
        .. math::
        
            2^{\\frac{7}{12}}
            
    is off by about 1.5 cents (which can be calculated by):
    
    .. code::
    
        ratio_to_cents(p5) - ratio_to_cents(edo_rep[2])
        
    **A Note on Constructors:**
    
    In general a degree has a character symbol, but there is one symbol
    that has semantic meaning: the inverse of a ratio. As an example, the
    constructors for the Lucy scale are defined in ``pytuning.constants`` as:
    
    .. code::

        lucy_construtors = [
            (lucy_L,               "L"  ),
            (lucy_s,               "s"  ),
            (sp.Integer(1)/lucy_L, "1/L"),
            (sp.Integer(1)/lucy_s, "1/s"),    
        ]
        
    Note that two of the symbols are inverse of the other. If the code
    sees a symbol in the form "1/X" is it assumed to be the inverse of "X".
    This is used for simplification, as, for example, the first line
    in the following simplifies to the second:
    
    .. code::
    
        # This expression:
        x = ['L','s','1/L']
        
        # Is equivalent to:
        x = ['s']
    '''
    intervals = [x[0] for x in constructors] + [sp.Integer(1)]
    possiblities = np.array([x for x in itertools.combinations_with_replacement(intervals, max_terms)])
    reduced = np.array([reduce(operator.__mul__,x) for x in possiblities])
    interval_sizes_numeric = np.array([float(x.evalf()) for x in reduced])
    distances = np.abs(interval_sizes_numeric - float(interval.evalf()))
    best_index = np.argmin(distances)
    target_compostion = list(possiblities[best_index])
    target_compostion = [x for x in filter(lambda x: x != sp.Integer(1), target_compostion)]
    mapper = dict([(x[0],x[1]) for x in constructors])
    inverse_mapper = dict([(x[1],x[0]) for x in constructors])
    symbolic = sorted([mapper[x] for x in target_compostion])
    
    # Simplify (which is to say, remove inversion*interval products)
    
    sym = np.array([x[1] for x in constructors])
    symbols = np.array(symbolic)
    count = []
    for ss in sym:
        if len(symbols) == 0:
            count = count + [0]
        else:
            count = count + [np.sum(symbols == ss)]
    counts          = dict(zip(sym, count))
    adjusted_counts = dict(zip(sym, count))

    for key in counts:
        if key[:2] != "1/":
            if ("1/"+key) in counts:
                number = max(0,counts[key] - counts["1/"+key])
            else:
                number = counts[key]
            adjusted_counts[key] = number
        if key[:2] == "1/":
            if (key[2:]) in counts:
                number = max(0,counts[key] - counts[key[2:]])
            else:
                number = counts[key]
            adjusted_counts[key] = number
    if "1" in adjusted_counts:
        del adjusted_counts["1"]

    adjusted_output = []
    for key in adjusted_counts:
        adjusted_output = adjusted_output + [key]*adjusted_counts[key]
    adjusted_output = sorted(adjusted_output)
    
    simplified_target = [inverse_mapper[x] for x in adjusted_output]
    if len(simplified_target) == 0:
        values = sp.Integer(1)
    else:
        values = reduce(operator.__mul__,simplified_target)
    return (simplified_target, adjusted_output, values)
    
def create_scale_from_scale(scale, interval_function, max_terms=8, tone_table=None):
    '''    
    Given a target scale, calculate the closest matching N-rank
    linear temperament scale over the provide basis functions.
    
    :param scale: The target scale (list or ratios)
    :param interval_function: The interval function (see below)
    :param max_terms: The maximum number of terms for the factoring
        along the basis intervals
    :param tone_table: A constrained tone table (see below)
    :returns: A tuple, the first member of which is a list
        of the derived scale values, and the second of which is
        a symbolic representation of the factoring found.
    
    The interval function is a function that accepts a degree and
    ``max_terms`` and returns the breakdown in the same format
    as ``find_factors``. In general the easiest way to create this
    function is thought a partial function application of
    ``find_factors`` and the specific constructors wanted.
    As an example, to create a function that will approimate a scale
    with the five-limit constructors:
    
    .. code::
    
        from pytuning.scale_creation import find_factors, create_scale_from_scale
        from pytuning.constants import five_limit_constructors
        import functools
        
        find_five_limit_interval = functools.partial(
            find_factors, constructors=five_limit_constructors,
            max_terms=15)
            
        create_five_limit_scale_from_scale = functools.partial(create_scale_from_scale, 
                                    interval_function=find_five_limit_interval)
                                    
    if ``tone_table`` is ``None``, the code will perform the factoring
    with up to ``max_terms``. If the tone table is defined only the
    intervals defined in this table will be used.
    
    The tone table is formatted as a list of tuples, where the members of each
    tuple are the degree name (``String``), the interval composition
    (a list of characters taken from the symbolic portion of
    the constructors), and the value of that factoring. As an
    example, the tone table that matches published values
    for the Lucy-tuned scale begins:
    
    .. code::
    
        [('1', [], 1),
         ('5', ['L', 'L', 'L', 's'], sqrt(2)*2**(1/(4*pi))),
         ('2', ['L'], 2**(1/(2*pi))),
         ('6', ['L', 'L', 'L', 'L', 's'], sqrt(2)*2**(3/(4*pi))),
         ('3', ['L', 'L'], 2**(1/pi)),
         ('7', ['L', 'L', 'L', 'L', 'L', 's'], sqrt(2)*2**(5/(4*pi))),
         ('#4', ['L', 'L', 'L'], 2**(3/(2*pi))), ...]
         
    (The last member of the tuple is a ``sympy`` symbolic value.)
    
    With the tone table, the code will return the defined tone
    which most closely matches the target degree.
    
    Extending the above example, if we were to try to match
    a Pythagorean scale with an unconstrained factoring of the
    Five-limit intervals (i.e., with no tone table):
    
    .. code::
    
        pythag = create_pythagorean_scale()
        lp = create_five_limit_scale_from_scale(pythag)
        
    yields
    
    .. code::
    
        ([1,
          16/15,
          9/8,
          32/27,
          81/64,
          4/3,
          1024/729,
          3/2,
          128/81,
          27/16,
          16/9,
          243/128,
          2],
         [[],
          ['s'],
          ['T'],
          ['s', 't'],
          ['T', 'T'],
          ['T', 's', 't'],
          ['s', 's', 't', 't'],
          ['T', 'T', 's', 't'],
          ['T', 's', 's', 't', 't'],
          ['T', 'T', 'T', 's', 't'],
          ['T', 'T', 's', 's', 't', 't'],
          ['T', 'T', 'T', 'T', 's', 't'],
          ['T', 'T', 'T', 's', 's', 't', 't']])
    '''
    output = []
    steps = []
    for degree in scale:
        if tone_table is None:
            interval = interval_function(degree, max_terms=max_terms)
            found_degree = interval[2]
            step = interval[1]
        else:
            distances = np.array([abs(1 - x[2]/degree).evalf() for x in tone_table])
            index = np.argmin(distances)
            found_degree = tone_table[index][2]
            step = tone_table[index][1]
        steps = steps + [step]
        output = output + [found_degree]
    output = [x.simplify() for x in output]
    return output, steps

