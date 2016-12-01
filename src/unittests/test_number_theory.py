#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 19:07:48 2016

@author: mark
"""

from __future__ import division, print_function

import unittest, sys

from pytuning.number_theory import find_prime_limit_for_scale, find_odd_limit_for_scale
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