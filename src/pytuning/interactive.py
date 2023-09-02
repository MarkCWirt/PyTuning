# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:23:12 2015

@author: mark
"""

# File to source into iPython for interactive console use
#
# Here we accomplish three things:
#
#  * Import the appropriate modules and make them available
#    to the interpreter
#
#  * Create some interactive convenience functions
#
#  * Establish a namespace for the convenience functions

from __future__ import print_function, division
from typing import List, Any
import sympy as sp

try:
    import matplotlib.pyplot as plt
    plt.ioff()
    get_ipython().magic(u'matplotlib')
except Exception:
    print("Warning: Matplotlib not available")

try:
    import seaborn as sns
    sns.set()
except Exception:
    print("Warning: Seaborn not available")

from pytuning.number_theory import *  # noqa
from pytuning.constants import *  # noqa
from pytuning.scales import *  # noqa
from pytuning.metrics import *  # noqa
from pytuning.tuning_tables import *  # noqa
from pytuning.scale_creation import find_best_modes, create_scale_from_scale, find_factors  # noqa
from pytuning.visualizations import consonance_matrix  # noqa

from pytuning.scales import *  # noqa
from pytuning.utilities import *  # noqa
from pytuning.constants import all_constructors

# In Python 3 raw_input has been named input
try:
    input = raw_input
except NameError:
    pass

sp.init_printing(use_unicode=True)

try:
    from IPython.display import display
except Exception:
    pass

__all__ = ["harmonic_scale", "intervals", "scale", "cents",
           "distinct_i", "generators", "Interval"]

# Global Variables

scale: List[Any] = []         # Current Scale
cents: List[Any] = []         # Cent values of current scale
distinct_i: List[Any] = []    # Distinct intervals
generators: List[Any] = []    # Linear temprement generators


def intervals():
    global scale
    global distinct_i
    if len(scale) == 0:
        print("Please create a scale first")
        return
    distinct_i = distinct_intervals(scale)
    display(distinct_i)


def harmonic_scale():
    '''
    Create a harmonic scale in an interactive environment.

    This function will prompt for the first and last harmonic, as well as
    the user's desire for normalization. It assumes the standard octave of 2.

    The output is put into the global ``scale``.
    '''

    global scale
    global cents
    first_harmonic = input("First harmonic: ")
    number_harmonics = input("Number of harmonics: ")
    normalize = input("Normalize? (y/n):")
    if len(normalize) == 0 or normalize[0] == 'Y' or normalize[0] == 'y':
        normalize = True
    else:
        normalize = False

    scale = create_harmonic_scale(
        int(first_harmonic),
        int(number_harmonics),
        normalize=normalize
    )
    print("Current Scale:")
    display(scale)
    cents = [ratio_to_cents(x) for x in scale]


def edo_scale():
    '''
    Create an EDO scale in an interactive environment.

    This function will prompt for the number of divisions (tones) and the
    formal octave.

    The output is put into the global ``scale``.
    '''
    global scale
    global cents
    number_tones = input("Number of tones: ")
    octave = input("Formal Octave (2):")

    if len(octave) == 0:
        octave = 2
    else:
        octave = int(octave)

    scale = create_edo_scale(int(number_tones), octave)

    print("Current Scale:")
    display(scale)
    cents = [ratio_to_cents(x) for x in scale]


def euler_fokker():
    '''
    Create a scale of the Euler Fokker Genus in an interactive environment.

    This function will prompt for generator primes and the
    formal octave. Note that multiplicities is not prompted for, so if there are
    repetitions they will need to be spelled out separately.

    The output is put into the global ``scale``.
    '''
    global scale
    global cents
    intervals = input("Intervals (list of prime integers): ")
    octave = input("Formal Octave (2):")

    if len(octave) == 0:
        octave = 2
    else:
        octave = int(octave)

    exec("int_parsed =%s" % intervals, globals())
    multiplicities = [1] * len(intervals)
    scale = create_euler_fokker_scale(int_parsed, multiplicities, octave)
    print("Current Scale:")
    display(scale)
    cents = [ratio_to_cents(x) for x in scale]


def set_generators():
    global generators
    index = 0
    for entry in all_constructors:
        print(index, entry[1])
        index = index + 1
    selected = input("Which generator?:")
    generators = all_constructors[int(selected)][0]
