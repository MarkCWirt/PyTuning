#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 09:45:13 2016

@author: mark
"""
# A Null test. Just make sure the file can be loaded (I've been bitten
# by that one before)


from __future__ import division, print_function

import unittest, sys

class TestInteractive(unittest.TestCase):
    
    def test_file_load(self):
        from pytuning.interactive import harmonic_scale
        
def suite():
    interactive_suite = unittest.TestLoader().loadTestsFromTestCase(TestInteractive)
    return interactive_suite

if __name__ == '__main__':
    print("******************************")
    print("Begining Interacive Test Suite")
    print("*******************************")
    interactive_suite = suite()
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    return_value =  not runner.run(interactive_suite).wasSuccessful()
    sys.exit(return_value)
