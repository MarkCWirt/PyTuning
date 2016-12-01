# -*- coding: utf-8 -*-
"""
Created on Tue May 26 11:08:37 2015

@author: mark
"""

import sympy as sp
import numpy as np

from pytuning.utilities import distinct_intervals, normalize_interval

__all__ = ["sum_p_q","sum_distinct_intervals","metric_3","sum_p_q_for_all_intervals",
           "sum_q_for_all_intervals"]

def sum_p_q(scale):
    '''    
    Calculate a metric for a scale
    
    :param scale: The scale.
    :returns: A ``dict`` with the metric value.
    
    This is an estimate of scale consonance. It is derived 
    from summing the numerators and denominators of the 
    scale degrees. 
    
    Smaller values are more consonant.
    
    Note that this metric looks at the degrees of the scale, so it is somewhat
    tonic-focused. The similar metric ``sum_p_q_for_all_intervals()`` is similar, 
    but it sums the numerator and denominator values for all distinct intervals within
    the scale.
    
    While the metric is numerically defined for ratios expressed as irrational or
    transcendental numbers, it is really only meaningful for scales with just
    degrees (ratios expressed as rational numbers).
    
    .. code:: python
        
        sum_p_q(create_pythagorean_scale())
        
    yields:
        
    .. code:: python
        
        {'sum_p_q': 3138}
        
    '''
    return {"sum_p_q": int(sum(map (lambda x: sum(list(sp.fraction(x))), scale)))}

def sum_distinct_intervals(scale):
    '''    
    Calculate a metric for a scale
    
    :param scale: The scale.
    :returns: A ``dict`` with the metric value.
        
    This metric is an estimate of scale consonance. Numerically
    it is the number of distinct intervals within the
    scale (including all ratios and their inversions).
    
    Smaller values are more consonant.
    
    .. code:: python
    
        sum_distinct_intervals(create_pythagorean_scale())
    
    yields:
    
    .. code:: python
    
        {'sum_distinct_intervals': 22}
    '''
    return {"sum_distinct_intervals": len(distinct_intervals(scale))}

def metric_3(scale):
    '''    
    Calculate a metric for a scale
    
    :param scale: The scale.
    :returns: A ``dict`` with the metric value.
    
    Metric 3 is an estimate of scale consonance. Given a
    ratio p/q, it is a heuristic given by the following:
    
    .. math::
    
        \\begin{align}
        m_3 &= \\sum{\\frac{1}{\\frac{p-q}{q}}}
        &= \\sum{\\frac{q}{p-q}}
        \\end{align}
    
    Smaller values are more consonant.
    
    The summation takes place over all of the intervals in the scale. It does not
    form a set of distinct intervals.
    '''
    
    return {"metric_3": sum([1/y for y in filter(
                    lambda x: x != 0, [(
                        sp.fraction(x)[0] - 
                        sp.fraction(x)[1])/
                        sp.fraction(x)[1] for x in scale])]).evalf()
            }

def sum_p_q_for_all_intervals(scale):
    '''    
    Calculate a metric for a scale
    
    :param scale: The scale (i.e., a list of ``sympy.Rational`` values)
    :returns: The metric.
    
    This metric is an estimate of scale consonance. It is formed by examining
    all unique intervals in the scale, and creating a numeric value based upon
    the summation of the numerators and denominators for all those intervals.
    
    While the metric is numerically defined for ratios expressed as irrational or
    transcendental numbers, it is really only meaningful for scales with just
    degrees (ratios expressed as rational numbers).
    
    Smaller values are more consonant.
    
    '''
    
    return {"sum_p_q_for_all_intervals": 
                int(sum(map (lambda x: sum(list(sp.fraction(x))), 
                distinct_intervals(scale))))
    }
                        
def sum_q_for_all_intervals(scale):
    '''    
    Calculate a metric for a scale.
    
    :param scale: The scale (i.e., a list of ``Rational`` s)
    :returns: The metric.
    
    Metric 5 is an estimate of scale consonance. It is summation
    of the denominators of the normalized distinct ratios
    of the scale.
    
    Smaller values are more consonant.
    '''
    m5 = np.sum([sp.fraction(normalize_interval(x))[1] 
        for x in distinct_intervals(scale)])
    
    return {"sum_q_for_all_intervals": m5}
                        
def all_metrics(scale):
    '''    
    Calculate all metrics for the scale
    
    :param scale: The scale (i.e., a list of ``Rational`` s)
    :returns: A ``dict`` containing all metrics.
    
    As an example:
    
    .. code::
    
        pythag = create_pythagorean_scale()
        metrics = all_metrics(pythag)
        
    will (currently) produce:
    
    .. code::
    
        {
         'metric_3': 49.9049074891784,
         'sum_distinct_intervals': 22,
         'sum_p_q': 3138,
         'sum_p_q_for_all_intervals': 1092732,
         'sum_q_for_all_intervals': 452817
        }
        
    If new metrics are coded they should be added to the ``__all__`` data member
    for inclusion here.
    '''
    output = {}
    for metric in __all__:
        output[metric] = list(globals()[metric](scale).values())[0]
    return output
