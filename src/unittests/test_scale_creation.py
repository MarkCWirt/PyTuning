#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 17:10:15 2016

@author: mark
"""

from __future__ import division, print_function

import unittest, sys
from functools import partial

import sympy as sp

from pytuning.scale_creation import find_best_modes, find_factors, create_scale_from_scale
from pytuning.constants import five_limit_constructors
from pytuning.scales import create_pythagorean_scale, create_diatonic_scale, \
    create_euler_fokker_scale

pythag_scale = create_pythagorean_scale()

five_limit_with_reciprocal = [
    (sp.Rational(16,15), "s"),
    (sp.Rational(10,9),  "t"),
    (sp.Rational(9,8),   "T"),
    (sp.Rational(15,16), "1/s"),
    (sp.Rational(9,10),  "1/t"),
    (sp.Rational(8,9),   "1/T"),
]

tone_table = [('1', [], sp.Integer(1)),
 ('2', ['2'], sp.Integer(2)),
 ('3', ['3'], sp.Integer(3)),
 ('5', ['5'], sp.Integer(4)),
 ('X', ['X'], sp.Integer(15))]
  
tone_constructors = [
    (sp.Integer(2),  '2'),
    (sp.Integer(3),  '3'),
    (sp.Integer(5),  '5'),
    (sp.Integer(15), 'X'),
]
  
class TestScaleCreatio(unittest.TestCase):
    
    def test_find_best_modes(self):
        # This is a null test. Just make sure it executes. Tests all the metrics
        find_best_modes(pythag_scale, 7)
        
    def test_factoring(self):
        interval = sp.Rational(16,15)
        factors = find_factors(interval, five_limit_constructors)
        self.assertListEqual(['s'], factors[1])
        interval = sp.Rational(10,9)
        factors = find_factors(interval, five_limit_constructors)
        self.assertListEqual(['t'], factors[1])
        interval = sp.Rational(9,8)
        factors = find_factors(interval, five_limit_constructors)
        self.assertListEqual(['T'], factors[1])
        
        interval = sp.Rational(16,15) * sp.Rational(10,9) * sp.Rational(9,8)
        factors = find_factors(interval, five_limit_constructors)
        self.assertTrue(len(factors[1]) == 3)
        for factor in factors[1]:
            self.assertTrue( factor in ['T', 's', 't'] )
            
        interval = sp.Rational(16,15) / sp.Rational(9,8)
        factors = find_factors(interval, five_limit_with_reciprocal)
        for factor in factors[1]:
            self.assertTrue( factor in ['1/T', 's'] )
        
    def test_create_scale_from_scale(self):
        # Use Ptolemy for the target scale
        scale = create_diatonic_scale(five_limit_constructors, ["T", "t", "s", "T", "t", "T", "s"])
        
        # Now recreate it with the same factor functions
        interval_function = partial(find_factors, constructors = five_limit_constructors)
        scale_derived = create_scale_from_scale(scale, interval_function)
        self.assertListEqual(scale, scale_derived[0])
        
    def test_create_scale_from_scale_with_tone_table(self):
        scale = create_euler_fokker_scale([3,5],[1,1], normalize=False)
        i_function = partial(find_factors, constructors = tone_constructors)
        derived_scale = create_scale_from_scale(scale, i_function, tone_table=tone_table)
        self.assertListEqual(derived_scale[1],[[], ['2'], ['3'], ['5'], ['X']])
        
def suite():
    scale_creation_suite = unittest.TestLoader().loadTestsFromTestCase(TestScaleCreatio)
    return scale_creation_suite

if __name__ == '__main__':
    print("*****************************")
    print("Begining Scale Creation Suite")
    print("*****************************")
    scale_creation_suite = suite()
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    return_value =  not runner.run(scale_creation_suite).wasSuccessful()
    sys.exit(return_value)
