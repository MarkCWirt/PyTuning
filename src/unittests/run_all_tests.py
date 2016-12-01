#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:44:35 2016

@author: mark
"""

import unittest, sys

if __name__ == '__main__':    
    test_suite = unittest.TestLoader().discover('.')
    test_runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
    return_value = not test_runner.run(test_suite).wasSuccessful()
    sys.exit(return_value)
