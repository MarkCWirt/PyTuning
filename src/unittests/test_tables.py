#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 16:18:36 2016

@author: mark
"""

# ***Note***: These are null tests. They made sure the code runs without 
# throwing an asertion, but they don't actually check the output. I may 
# improve this at some point, but checking strings is fragile.

from __future__ import division, print_function

import unittest, sys
from pytuning.tuning_tables import create_scala_tuning, create_csound_tuning, create_em_tuning, \
    create_fluidsynth_tuning, create_timidity_tuning
from pytuning.scales import create_edo_scale, create_pythagorean_scale

# For each table we'll check a rational and irrational scale, as they are
# handeled differently for some tuning tables.

pythag = create_pythagorean_scale()
edo    = create_edo_scale(12)

class TestTables(unittest.TestCase):
    
    def test_scala_tuning(self):
        create_scala_tuning(pythag, "Pythagorean Scale")
        create_scala_tuning(edo, "12-TET")
        
    def test_csount_tuning(self):
        create_csound_tuning(pythag)
        create_csound_tuning(edo)
        create_csound_tuning(pythag, reference_note=69)
        create_csound_tuning(edo, reference_note=69)
        
    def test_em_tuning(self):
        create_em_tuning(pythag)
        create_em_tuning(edo)
        create_em_tuning(pythag, reference_note=69)
        create_em_tuning(edo, reference_note=69)
        
    def test_fluid_tuning(self):
        create_fluidsynth_tuning(pythag)
        create_fluidsynth_tuning(edo)
        create_fluidsynth_tuning(pythag, reference_note=69)
        create_fluidsynth_tuning(edo, reference_note=69)
    
    def test_timidity_tuning(self):
        create_timidity_tuning(pythag)
        create_timidity_tuning(edo)
        create_timidity_tuning(pythag, reference_note=69)
        create_timidity_tuning(edo, reference_note=69)
    
def suite():
    table_suite = unittest.TestLoader().loadTestsFromTestCase(TestTables)
    return table_suite

if __name__ == '__main__':
    print("*************************")
    print("Begining Table Test Suite")
    print("*************************")
    table_suite = suite()
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    return_value =  not runner.run(table_suite).wasSuccessful()
    sys.exit(return_value)