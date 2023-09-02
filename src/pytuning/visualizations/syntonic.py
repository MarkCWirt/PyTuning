# -*- coding: utf-8 -*-
"""
Created on Tue May 26 12:28:53 2015

@author: vagrant
"""

from __future__ import print_function, division

try:
    import matplotlib.pyplot as plt   # type: ignore
except Exception:
    print("Warning: Matplotlib not found.Plotting will not be available")
import numpy as np

from pytuning.scales.equal_interval import create_equal_interval_scale
from pytuning.utilities import ratio_to_cents, cents_to_ratio

try:
    import seaborn as sns  # type: ignore
    sns.set()
except Exception:
    print("Warning: Seaborn not available.")

try:
    from sklearn.cluster import MeanShift  # type: ignore
except Exception:
    print("WARNING: Scikit-learn not available.")


def plot_syntonic_intervals(scale_length, min_g, max_g, number_g):
    generators = np.linspace(min_g, max_g, num=number_g)
    ratio_generators = [cents_to_ratio(x) for x in generators]

    # Calculations

    x = [create_equal_interval_scale(
        x, scale_length, sort=False, remove_duplicates=False) for x in ratio_generators]
    # Graphics

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.grid(True)

    for index in range(scale_length + 1):
        data = [ratio_to_cents(d[index]) for d in x]
        plt.plot(generators, data)
    plt.xlabel("Generating Interval (Cents)")
    plt.ylabel("Degree Size (Cents)")
    plt.title("Relationship of Syntonic Tuning to Generator Size")
    plt.xlim([generators[0], generators[-1]])
    plt.ylim([0, 1200])
    return fig


def cluster_syntonic(generators, scale_length=13, bandwidth=0.005):
    output = []
    x = [create_equal_interval_scale(x, scale_length) for x in [cents_to_ratio(x) for x in generators]]

    for index in range(len(x)):
        data = x[index]
        q = np.array(data)
        q.shape = (len(q), 1)
        ms = MeanShift(bandwidth=bandwidth)
        ms.fit(q)
        output = output + [len(ms.cluster_centers_)]
    return generators, np.array(output)


def plot_syntonic_data(generators, scale_length=13, bandwidth=0.005,
                       ylab="Number of Discrete Steps"):
    g, data = cluster_syntonic(generators, scale_length=scale_length,
                               bandwidth=bandwidth)
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.grid(True)
    plt.plot(generators, data - 1)
    plt.xlabel("Generating Interval (Cents)")
    plt.ylabel(ylab)
    plt.title("Relationship of Syntonic Tuning to Generator Size")
    plt.xlim([generators[0], generators[-1]])
    plt.ylim([float(np.min(data) - 1), float(np.max(data) - 1)])
    return fig
