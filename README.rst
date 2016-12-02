PyTuning
========

|build|

PyTuning is a Python library intended for the exploration of musical scales
and microtonalities. It can be used by developers who need ways of calculating,
analyzing, and manipulating musical scales, but it can also be used interactively.

It makes heavy use of the `SymPy <http://www.sympy.org/>`__ package, a pure-Python
computer algebra system, which allows scales and scale degrees to be
manipulated symbolically, with no loss of precision. There is also an optional
dependency on `Matplotlib <http://matplotlib.org/>`__ (and
`Seaborn <http://seaborn.pydata.org/>`__) for some visualizations that have been
included in the package.

Some of the package's features include:

* Creation of scales in a variety of ways (EDO, Euler-Fokker, Diatonic, Harmonic,
  from generator intervals, etc.)
* Ability to represent created scales in ways that are understood by external
  software (Scala, Timidity, Fluidsynth, Yoshimi, Zynaddsubfx).
* Some analysis functions (for example, PyTuning provides a framework for searching
  for scale modes based upon defined metric functions and combinatorial analysis). Also
  included are some number-theoretic functions, such as prime limits and odd limits.
* Some scale visualizations.
* Interactive use.


As a simple example, to create a 31-TET scale and then create a tuning table for
the timidity soft-synth:

.. code:: python

  scale = create_edo_scale(31)
  tuning_table = create_timidity_tuning(scale, reference_note=69)

The design of PyTuning is purposefully simple so that non-computer professionals can
use it without much difficultly (musicians, musicologist, interested people of all
stripes).

In scope this project is similar to the `Scala <http://www.huygens-fokker.org/scala/>`__
software package, with a few differences:

* Scala is a mature, full-featured package that includes many, many scales
  and functions for manipulating and analyzing those scales. This project
  is much newer and less mature; it's scope is currently much less (but
  hopefully it will be easy to extend).
* PyTuning is written in Python and relies on modern, well maintained dependencies.
  Scala is written in Ada, and while this is an interesting choice, it probably
  limits the population of users who *could* change or extend it should a need
  arise.
* Scala is mainly an application. PyTuning is a development library, but with
  ways for non-programmers to use it interactively.
* This package does *not* interact with sound cards or audio drivers, so one
  can't play a scale directly. There are, however,
  functions for exporting scales into other software packages so that music
  and sound can be produced.

Installation
------------

PyTuning runs under Python 2.7.X and 3.X.

The easiest way to install PyTuning is via the Python Package Index, with
which Pytuning is `registered <https://pypi.python.org/pypi/PyTuning/>`__:

.. code:: bash

  pip install pytuning

There are two hard dependencies for PyTuning: `SymPy <http://www.sympy.org/en/index.html>`__ and
`NumPy <http://www.numpy.org/>`__. SymPy is a pure Python library and ``pip`` will handle
it's installation nicely. NumPy is a more complicated package and if installed via ``pip`` may
involve much compilation; it would probably behoove you to install the package manually via
whatever mechanism your platform provides before ``pip`` installing the package .

If you are running the package interactively it is recommended that the Jupyter interactive
shell be installed. This is discussed in the documentation under the notes on Interactive use.

The source-code is available on `GitHub <https://github.com/MarkCWirt/PyTuning>`__, where
it can be cloned and installed.

Documentation
-------------

Documentation for the package can be found on `Read the Docs <http://pytuning.readthedocs.io/>`__.


Roadmap
-------

More scales, more visualizations, more analysis functions. Pull requests are welcome!


.. |build| image:: https://travis-ci.org/MarkCWirt/PyTuning.svg?branch=master
   :target: https://travis-ci.org/MarkCWirt/PyTUning
