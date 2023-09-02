# -*- coding: utf-8 -*-
"""
Created on Sun May 31 10:57:14 2015

@author: mark
"""
from __future__ import print_function, division

import copy
import sympy as sp
import numpy as np

from pytuning.utilities import normalize_interval

my_palette = np.array([np.array([0.13333333, 0.13333333, 0.13333333, 1.]),
                       np.array([0.31836986, 0.06640523, 0.31836986, 1.]),
                       np.array([0.50196078, 0., 0.50196078, 1.])])
try:
    import matplotlib.pyplot as plt   # type: ignore
    import matplotlib                 # type: ignore
    my_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("Default", my_palette)
except Exception:
    print("Wanring: Matplotlib not found.Plotting will not be available")


try:
    import seaborn as sns   # type: ignore
    sns.set()
    my_palette = sns.dark_palette('purple', 10)
    my_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("Default", my_palette)
except Exception:
    print("Warning: Seaborn not available.")


def metric_denom(degree):
    '''
    .. py:function:: metric_denom(degree)

        Calculate a metric for the consonance heatmap. This metric is just the
        denominator of the normalized ratio. It is also the default
        metric if none is specified.

        :param scale: The degree (a frequency ratio)
        :returns: The metric
    '''
    normalized_degree = normalize_interval(degree)
    # y = sp.fraction(normalized_degree)[0] - sp.fraction(normalized_degree)[1]
    y = sp.fraction(normalized_degree)[1]
    return y


def consonance_matrix(scale, metric_function=None, figsize=(10, 8),
                      title="Consonance Matrix", annot=True, cmap=None,
                      fig=None, vmin=None, vmax=None):
    '''
    Display a consonance matrix for a scale

    :param scale: The scale to analyze (list of frequency ratios)
    :param metric_function: The metric function (see below)
    :param figsize: Size of the figure (tuple, in inches)
    :param title: the graph title
    :param annot: If `True`, display the value of the metric in the
        grid cell
    :param cmap: A custom ``matplotlib`` colormap, if desired
    :param fig: a ``matplotlib.figure.Figure`` or ``None``. If ``None``
        a figure will be created
    :param vmin: If secified, the lowest value of the range to plot. Only
        works if Seaborn is included.
    :param vman: If secified, the largest value of the range to plot. Only
        works if Seaborn is included.
    :returns: a ``matplotlib.Figure`` for display

    The consonance matrix is created by taking each scale degree
    along the bottom and left edges of a matrix, forming a frequency
    ratio between the left and bottom value, and applying the
    metric function to that value.

    The default metric function is the denominator of the normalized
    ratio -- the thought being that the smaller this number is the
    more consonant the interval.

    If a user-specified metric function is used, that function
    should accept one parameter (the ratio) and return one value.
    As an example, the default metric function:

    .. code::

        def metric_denom(degree):
            normalized_degree = normalize_interval(degree)
            return sympy.fraction(normalized_degree)[1]

    Note that, as with most parts of this code, the ratios
    should be expressed in terms of ``sympy`` values, usually
    ``sympy.Rational``'s

    A note of figures: With the default of fig=None, this function
    will just produce a figure and return it for display. However,
    if one wants to plot multiple figures and can pre-allocate it.
    This is useful, for example, if one wants to plot multiple
    figures on the same chart. As an example, the following will plot
    two separate consonance matrices, side-by-side:

    .. code::

        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(15,6))
        plt.subplot(plt.GridSpec(1, 2)[0,0])
        fig = consonance_matrix(scale,title="Full Scale", fig=fig)
        plt.subplot(plt.GridSpec(1, 2)[0,1])
        fig = consonance_matrix(mode_scale,title="Mode Scale", fig=fig)
        fig

    ``vmin`` and ``vmax`` are useful if you're plotting multiple graphs in
    the same figure; they can be used to ensure that all the component graphs
    use the same scale, so that visually the graphs are related. Otherwise each
    graph will have its own scale.

    '''
    xticklabels = ["%s" % x for x in scale]
    data = np.zeros((len(scale), len(scale)))
    for index1 in range(len(scale)):
        for index2 in range(len(scale)):
            entry = scale[index1] / scale[index2]
            if metric_function is not None:
                entry_value = metric_function(entry)
            else:
                entry_value = metric_denom(entry)
            data[index1][index2] = entry_value
    if fig is None:
        fig = plt.figure(figsize=figsize)
        fig.add_subplot(1, 1, 1)

    plt.title(title)

    # reverse the y axis, as this is more intuitive
    data = data.tolist()
    data.reverse()
    data = np.array(data)
    yticklabels = copy.deepcopy(xticklabels)
    yticklabels.reverse()
    if cmap is None:
        cmap_to_use = my_cmap
    else:
        cmap_to_use = cmap
    if vmin is None:
        if "sns" in globals():
            sns.heatmap(
                data, cmap=cmap_to_use, xticklabels=xticklabels,
                yticklabels=yticklabels, annot=annot)
        else:
            plt.imshow(data, cmap=cmap_to_use, interpolation="nearest")
            plt.xticks(np.arange(len(xticklabels)), xticklabels)
            plt.yticks(np.arange(len(yticklabels)), yticklabels)
            for y in range(data.shape[0]):
                for x in range(data.shape[1]):
                    plt.text(x, y, '%d' % data[y, x],
                             horizontalalignment='center',
                             verticalalignment='center',
                             color="white",
                             )
    else:
        if "sns" in globals():
            sns.heatmap(
                data, cmap=cmap_to_use, xticklabels=xticklabels,
                yticklabels=yticklabels, annot=annot, vmin=vmin, vmax=vmax)
        else:
            plt.imshow(data, cmap=cmap_to_use, interpolation="nearest")
            plt.xticks(np.arange(len(xticklabels)), xticklabels)
            plt.yticks(np.arange(len(yticklabels)), yticklabels)
            for y in range(data.shape[0]):
                for x in range(data.shape[1]):
                    plt.text(x, y, '%d' % data[y, x],
                             horizontalalignment='center',
                             verticalalignment='center',
                             color="white",
                             )

    return fig


if __name__ == '__main__':
    from IPython.display import display    # type: ignore
    from pytuning.scales import create_harmonic_scale
    try:
        get_ipython().magic('matplotlib inline')
        scale = create_harmonic_scale(3, 10)
        fig = consonance_matrix(scale)
        display(fig)
    except Exception as e:
        print("iPython not aviailable")
        print(e)
