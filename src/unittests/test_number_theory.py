#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 19:07:48 2016

@author: mark
"""

from __future__ import division, print_function

import unittest, sys

import sympy as sp

from pytuning.number_theory import find_prime_limit_for_scale, find_odd_limit_for_scale, \
    prime_factor_ratio, create_ratio_from_primes

from pytuning.constants import syntonic_comma

from pytuning.scales import create_euler_fokker_scale

class TestNumberTheory(unittest.TestCase):
    
    def test_prime_limits(self):
        scale = create_euler_fokker_scale([3,4,5], [2,2,2])
        self.assertEqual(5, find_prime_limit_for_scale(scale))
        scale = create_euler_fokker_scale([3,4,5,7], [2,2,2,2])
        self.assertEqual(7, find_prime_limit_for_scale(scale))
        scale = create_euler_fokker_scale([3,4,5,11], [2,2,2,2])
        self.assertEqual(11, find_prime_limit_for_scale(scale))
        
    def test_odd_limits(self):
        scale = create_euler_fokker_scale([3,4,5], [2,2,2])
        self.assertEqual(225, find_odd_limit_for_scale(scale))
        scale = create_euler_fokker_scale([3,4,5,7], [2,2,2,2])
        self.assertEqual(11025, find_odd_limit_for_scale(scale))
        scale = create_euler_fokker_scale([3,4,5,11], [2,2,2,2])
        self.assertEqual(27225, find_odd_limit_for_scale(scale))
        
    def test_prime_factor(self):
        r = syntonic_comma
        q1 = prime_factor_ratio(r)
        q2 = prime_factor_ratio(r, return_as_vector=True)
        self.assertDictEqual(q1, {2: -4, 3: 4, 5: -1})
        self.assertTupleEqual(q2, (-4, 4, -1))
        self.assertEqual(r, create_ratio_from_primes(q1))
        self.assertEqual(r, create_ratio_from_primes(q2))
        r = sp.Rational(243,224)
        q1 = prime_factor_ratio(r)
        q2 = prime_factor_ratio(r, return_as_vector=True)
        self.assertDictEqual(q1, {2: -5, 3: 5, 7: -1})
        self.assertTupleEqual(q2, (-5, 5, 0, -1))
        self.assertEqual(r, create_ratio_from_primes(q1))
        self.assertEqual(r, create_ratio_from_primes(q2))
        r = sp.Rational(59049,57344)
        q1 = prime_factor_ratio(r)
        q2 = prime_factor_ratio(r, return_as_vector=True)
        self.assertDictEqual(q1, {2: -13, 3: 10, 7: -1})
        self.assertTupleEqual(q2, (-13, 10, 0, -1))
        self.assertEqual(r, create_ratio_from_primes(q1))
        self.assertEqual(r, create_ratio_from_primes(q2))
        r = sp.Rational(128,125)
        q1 = prime_factor_ratio(r)
        q2 = prime_factor_ratio(r, return_as_vector=True)
        self.assertDictEqual(q1, {2: 7, 5: -3})
        self.assertTupleEqual(q2, (7, 0, -3))
        self.assertEqual(r, create_ratio_from_primes(q1))
        self.assertEqual(r, create_ratio_from_primes(q2))
        
def suite():
    number_suite = unittest.TestLoader().loadTestsFromTestCase(TestNumberTheory)
    return number_suite

if __name__ == '__main__':
    print("****************************")
    print("Begining Number Theory Suite")
    print("****************************")
    number_suite = suite()
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    return_value =  not runner.run(number_suite).wasSuccessful()
    sys.exit(return_value)