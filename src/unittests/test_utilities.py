#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 16:33:41 2016

@author: mark
"""

from __future__ import division, print_function

import unittest
import sys

import sympy as sp

try:
    power = sp.power    # type: ignore
except AttributeError:
    power = sp

from pytuning.utilities import normalize_interval, distinct_intervals, get_mode_masks, mask_scale, \
    mask_to_steps, ratio_to_cents, cents_to_ratio, note_number_to_freq, \
    compare_two_scales, ratio_to_name

from pytuning.scales import create_edo_scale

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

masked_pythag_scale = [
    sp.Integer(1),
    sp.Rational(9, 8),
    sp.Rational(81, 64),
    sp.Rational(4, 3),
    sp.Rational(3, 2),
    sp.Rational(27, 16),
    sp.Rational(243, 128),
    sp.Integer(2),
]


class TestUtilities(unittest.TestCase):

    def test_normalize(self):
        self.assertEqual(sp.Rational(3, 2), normalize_interval(3))
        self.assertEqual(sp.Rational(9, 8), normalize_interval(9))
        self.assertEqual(sp.Rational(21, 16), normalize_interval(21))

    def test_distinct_intervals(self):
        self.assertListEqual([sp.sqrt(2)], distinct_intervals(create_edo_scale(2)))
        self.assertTrue(power.Pow(2, sp.Rational(1, 3)) in distinct_intervals(create_edo_scale(3)))
        self.assertTrue(power.Pow(2, sp.Rational(2, 3)) in distinct_intervals(create_edo_scale(3)))

    def test_mode_masks(self):
        masks = [(0, 1, 6), (0, 2, 6), (0, 3, 6), (0, 4, 6), (0, 5, 6)]
        calculated_masks = get_mode_masks(7, 3)
        for mask in calculated_masks:
            self.assertTrue(mask in masks)

    def test_mask_scales(self):
        self.assertListEqual(masked_pythag_scale, mask_scale(pythag_scale, (0, 2, 4, 5, 7, 9, 11, 12)))

    def test_mask_to_steps(self):
        self.assertListEqual([2, 2, 1, 2, 2, 2, 1], mask_to_steps([0] * 13, (0, 2, 4, 5, 7, 9, 11, 12)))
        self.assertListEqual([2, 2, 8], mask_to_steps([0] * 13, (0, 2, 4)))

    def test_ratio_to_cents(self):
        self.assertEqual(0, ratio_to_cents(1))
        self.assertEqual(0, ratio_to_cents(sp.Integer(1)))
        self.assertEqual(1200, ratio_to_cents(2))
        self.assertEqual(1200, ratio_to_cents(sp.Integer(2)))
        self.assertAlmostEqual(701.95500086, ratio_to_cents(sp.Rational(3, 2)))

    def test_cents_to_ratio(self):
        # We have reason to believe that ratio_to_cents is working, so we'll just
        # transmogrify

        r = 1
        self.assertEqual(r, cents_to_ratio(ratio_to_cents(r)))
        r = 1.5
        self.assertEqual(r, cents_to_ratio(ratio_to_cents(r)))
        r = 1.75
        self.assertEqual(r, cents_to_ratio(ratio_to_cents(r)))
        r = 2
        self.assertEqual(r, cents_to_ratio(ratio_to_cents(r)))

    def test_note_number_to_freq(self):
        self.assertAlmostEqual(440.0, note_number_to_freq(69))
        self.assertAlmostEqual(440.0 / 2.0, note_number_to_freq(69 - 12))
        self.assertAlmostEqual(261.6255653005, note_number_to_freq(60))
        self.assertAlmostEqual(261.6255653005 / 2.0, note_number_to_freq(60 - 12))

    def test_compare_scales(self):
        # A null test. Just make sure it runs
        compare_two_scales(pythag_scale, pythag_scale)

    def test_ratio_to_name(self):
        self.assertEqual("Perfect Fifth", ratio_to_name(sp.Rational(3, 2)))
        self.assertTrue(ratio_to_name(sp.Integer(12)) is None)


def suite():
    utility_suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilities)
    return utility_suite


if __name__ == '__main__':
    print("*************************")
    print("Beginning Utilities Suite")
    print("*************************")
    utility_suite = suite()
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    return_value = not runner.run(utility_suite).wasSuccessful()
    sys.exit(return_value)
