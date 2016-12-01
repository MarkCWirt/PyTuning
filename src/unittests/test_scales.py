#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 15:21:58 2016

@author: mark
"""

from __future__ import division, print_function

import unittest, sys, copy
import sympy as sp

from pytuning.scales import create_harmonic_scale, create_edo_scale, \
    create_pythagorean_scale, create_equal_interval_scale, create_diatonic_scale, \
    create_quarter_comma_meantone_scale, create_euler_fokker_scale
    
from pytuning.constants import five_limit_constructors

from pytuning.scales.meantone import convert_p5_to_r, convert_r_to_p5 # Not tested elsewhere

# Some of these tests aren't very good, as they just make sure things run and
# don't do much detailed checking.

# I'll also hand-create a scale or two,

pythag_scale = [
    sp.Integer(1),
    sp.Rational(256, 243),
    sp.Rational(9, 8),
    sp.Rational(32, 27),
    sp.Rational(81, 64),
    sp.Rational(4, 3),
    sp.Rational(1024, 729),
    sp.Rational(3, 2),
    sp.Rational(128, 81),
    sp.Rational(27, 16),
    sp.Rational(16, 9),
    sp.Rational(243, 128),
    sp.Integer(2),
]

ptolemy = [
    sp.Integer(1),
    sp.Rational(9, 8),
    sp.Rational(5, 4),
    sp.Rational(4, 3),
    sp.Rational(3, 2),
    sp.Rational(5, 3),
    sp.Rational(15, 8),
    sp.Integer(2),
]

class TestScales(unittest.TestCase):
    
    def test_harmonic_scale(self):
        # A non-normalized harmonic scale. Easy to test
        scale = create_harmonic_scale(1,4, normalize=False)
        self.assertEqual(sp.Integer(1),    scale[0])
        self.assertEqual(sp.Integer(2),    scale[1])
        self.assertEqual(sp.Integer(3),    scale[2])
        self.assertEqual(sp.Integer(4),    scale[3])
        
        # A normalized scale
        scale = create_harmonic_scale(1,4)
        self.assertEqual(sp.Integer(1),    scale[0])
        self.assertEqual(sp.Rational(3,2), scale[1])
        self.assertEqual(sp.Integer(2),    scale[2])
        
        # Now a non-standard octave
        scale = create_harmonic_scale(1,4, octave=3)
        self.assertEqual(sp.Integer(1),    scale[0])
        self.assertEqual(sp.Rational(4,3), scale[1])
        self.assertEqual(sp.Integer(2),    scale[2])
        self.assertEqual(sp.Integer(3),    scale[3])
        
    def test_edo_scale(self):
        # They are all normalized, by defintion
        scale = create_edo_scale(2)
        self.assertEqual(sp.Integer(1),    scale[0])
        self.assertEqual(sp.sqrt(2),       scale[1])
        self.assertEqual(sp.Integer(2),    scale[2])
        
        # Non-standard octave
        scale = create_edo_scale(2, octave=3)
        self.assertEqual(sp.Integer(1),    scale[0])
        self.assertEqual(sp.sqrt(3),       scale[1])
        self.assertEqual(sp.Integer(3),    scale[2])
        
    def test_pythagorean_scale(self):
        scale = create_pythagorean_scale()
        self.assertListEqual(scale, pythag_scale)
        
        # Dimished fifth vs. augemnted fourth
        pythag_2 = copy.deepcopy(pythag_scale)
        pythag_2[6] = sp.Rational(729, 512)
        scale = create_pythagorean_scale(number_down_fifths=5)
        self.assertListEqual(scale, pythag_2)
        
    def test_equal_interval(self):
        # we'll just create the pythag....
        scale = create_equal_interval_scale(sp.Rational(3,2),12)
        self.assertListEqual(scale, pythag_scale)
        scale = create_equal_interval_scale(sp.Rational(3,2), 
                                            normalize=False, scale_size=3, 
                                            number_down_intervals=0)
        self.assertListEqual(scale, [sp.Integer(1), sp.Rational(3,2),
                                     sp.Integer(2), sp.Rational(9,4)])
        scale = create_equal_interval_scale(sp.Rational(3,2), 
                                            normalize=False, 
                                            scale_size=3, 
                                            number_down_intervals=0, 
                                            epsilon=1)
        self.assertListEqual(scale, [sp.Integer(1), sp.Integer(2)])
        
    def test_diatonic_scale(self):
        scale = create_diatonic_scale(five_limit_constructors, ["T", "t", "s", "T", "t", "T", "s"])
        self.assertListEqual(scale, ptolemy)
    
    def test_diatonic_scale_with_string(self):
        scale1 = create_diatonic_scale(five_limit_constructors, ["T", "t", "s", "T", "t", "T", "s"])
        scale2 = create_diatonic_scale(five_limit_constructors, "TtsTtTs")
        self.assertListEqual(scale1, scale2)
        
    def test_meantone_scale(self):
        scale = create_quarter_comma_meantone_scale()
        
        # Feeling lazy, so I'll just check a few
        self.assertEqual(sp.Integer(1),                     scale[0])
        self.assertEqual(sp.sqrt(5)/2,                      scale[2])
        self.assertEqual(sp.Rational(5,4),                  scale[4])
        self.assertEqual(sp.Integer(5) ** sp.Rational(1,4), scale[7])
        self.assertEqual(sp.Integer(2),                     scale[12])
        
    def test_meantone_p_and_r(self):
        p5 = 1
        self.assertEqual(p5, convert_r_to_p5(convert_p5_to_r(p5)))
        p5 = 2
        self.assertEqual(p5, convert_r_to_p5(convert_p5_to_r(p5)))
        p5 = 3
        self.assertEqual(p5, convert_r_to_p5(convert_p5_to_r(p5)).evalf())
        p5 = 4
        self.assertEqual(p5, convert_r_to_p5(convert_p5_to_r(p5)).evalf())
        
        
    def test_euler_fokker(self):
        scale = create_euler_fokker_scale([3,5],[1,1])
        self.assertEqual(sp.Integer(1),     scale[0])
        self.assertEqual(sp.Rational(5,4),  scale[1])
        self.assertEqual(sp.Rational(3,2),  scale[2])
        self.assertEqual(sp.Rational(15,8), scale[3])
        self.assertEqual(sp.Integer(2),     scale[4])

        scale = create_euler_fokker_scale([3,5],[1,1], octave=3)
        self.assertEqual(sp.Integer(1),     scale[0])
        self.assertEqual(sp.Rational(5,3),  scale[1])
        self.assertEqual(sp.Integer(3),     scale[2])
        
        scale =  create_euler_fokker_scale([3,5],[1,1],
                                           normalize=False, octave=3)
        self.assertListEqual(scale, [sp.Integer(1),sp.Integer(3),
                                     sp.Integer(5),sp.Integer(15)])
        
        scale = create_euler_fokker_scale([3,5],[0,0])
        self.assertListEqual(scale, [sp.Integer(1),sp.Integer(2)])
        
def suite():
    scale_suite = unittest.TestLoader().loadTestsFromTestCase(TestScales)

    return scale_suite

if __name__ == '__main__':
    print("*************************")
    print("Begining Scale Test Suite")
    print("*************************")
    scale_suite = suite()
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    return_value =  not runner.run(scale_suite).wasSuccessful()
    sys.exit(return_value)

