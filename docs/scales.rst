Scale Creation
==============

There are several scale-creation functions in the package. They are found in
``pytuning.scales`` and can be imported into the program's namespace with

.. code:: python

  from pytuning.scales import *

(Note that for interactive use these are imported by default).

The Harmonic Scale
------------------

We'll start with the harmonic scale; it will illustrate many of the concepts
used in scale creation.

There are two important concepts to understand:

* Normalization: If a scale is normalized (which is the default in all cases),
  then the intervals of the scale are normalized to fall within a single octave.
  This means scaling the interval either up or down the number of octaves needed
  to make the interval fall between the unison and the octave.
* The Octave: Normally an octave is defined as a doubling of frequency (:math:`2`),
  but it is possible to define an octave by some other number. If this is the case
  the normalization will takes place over this new octave.

The function to create a harmonic scale is, ``create_harmonic_scale``:

.. autofunction:: pytuning.scales.create_harmonic_scale

As an example, if we create a non-normalized harmonic scale of 10 harmonics:

.. code:: python

  harmonic_scale = create_harmonic_scale(1, 10, normalize=False)

We have the following scale:

.. math::

  \left [ 1, \quad 2, \quad 3, \quad 4, \quad 5, \quad 6, \quad 7,
  \quad 8, \quad 9, \quad 10\right ]

If we normalize it each interval is scaled by a power of two to fall within 1
and 2. So, for example, the :math:`9` becomes :math:`\frac{9}{8}`, because the
nine must be scaled by three octaves to fall within that range:

.. math::

  \frac{9}{8} = \frac{9}{2^3}

So the normalized scale is:

.. math::

    \left [ 1, \quad \frac{9}{8}, \quad \frac{5}{4}, \quad
    \frac{3}{2}, \quad \frac{7}{4}, \quad 2\right ]

But if we change our octave definition to be :math:`3`, we normalize on powers
of 3:

.. code:: python

  harmonic_scale = create_harmonic_scale(1, 10, octave=3)

yields:

.. math::

  \left [ 1, \quad \frac{10}{9}, \quad \frac{4}{3}, \quad \frac{5}{3},
  \quad 2, \quad \frac{7}{3}, \quad \frac{8}{3}, \quad 3\right ]

Equal Divsion of the Octave (Equal Temprament)
----------------------------------------------

Equal temperament scales can be created with the ``create_edo_scale()``
function. Note that this function does *not* accept a ``normalize`` argument, because
EDO scales are normalized by definition. If does, however, allow you to change the
definition of the formal octave.

.. autofunction:: pytuning.scales.create_edo_scale

Scales from a Generator Interval
--------------------------------

The ``create_equal_interval_scale()`` function will generate a scale from a
generator interval. This is the base function for several other scale types
(for example, the Pythagorean scale is created with a generator interval
of :math:`\frac{3}{2}`).

In he creation of a scale, the generator interval can either be used
directly (for, for example, making each successive tone a generator
interval above the previous tone), or in an inverted sense (making each
interval a generator *down* from the previous). This function starts
from the unison and walks down the number specified, walking up for the rest
of the intervals.

.. autofunction:: pytuning.scales.create_equal_interval_scale

The Pythagorean Scale
---------------------

This is the standard Pythagorean scale. Note that we can choose the number of
up and down intervals in the scale. The default yields the standard scale, with the
fourth degree as a diminished fifth, as opposed to the augmented fourth.

.. autofunction:: pytuning.scales.create_pythagorean_scale

So, for the standard scale we can use:

.. code:: python

  scale = create_pythagorean_scale()

yielding:

.. math::

  \left [ 1, \quad \frac{256}{243}, \quad \frac{9}{8}, \quad \frac{32}{27}, \quad
  \frac{81}{64}, \quad \frac{4}{3}, \quad \frac{1024}{729},
  \quad \frac{3}{2}, \quad \frac{128}{81}, \quad \frac{27}{16},
  \quad \frac{16}{9}, \quad \frac{243}{128}, \quad 2\right ]

If we wanted the augmented fourth:

.. code:: python

  scale = create_pythagorean_scale(number_down_fifths=5)

yielding:

.. math::

  \left [ 1, \quad \frac{256}{243}, \quad \frac{9}{8}, \quad \frac{32}{27},
  \quad \frac{81}{64}, \quad \frac{4}{3}, \quad \frac{729}{512},
  \quad \frac{3}{2}, \quad \frac{128}{81}, \quad \frac{27}{16},
  \quad \frac{16}{9}, \quad \frac{243}{128}, \quad 2\right ]

The Quarter-Comma Meantone Scale
--------------------------------

.. autofunction:: pytuning.scales.create_quarter_comma_meantone_scale

An example of use:

.. code:: python

  scale = create_quarter_comma_meantone_scale()

yields:

.. math::

  \left [ 1, \quad \frac{8}{25} 5^{\frac{3}{4}}, \quad \frac{\sqrt{5}}{2},
  \quad \frac{4 \sqrt[4]{5}}{5}, \quad \frac{5}{4}, \quad \frac{2}{5} 5^{\frac{3}{4}},
  \quad \frac{16 \sqrt{5}}{25}, \quad \sqrt[4]{5},
  \quad \frac{8}{5}, \quad \frac{5^{\frac{3}{4}}}{2},
  \quad \frac{4 \sqrt{5}}{5}, \quad \frac{5 \sqrt[4]{5}}{4},
  \quad 2\right ]

Euler-Fokker Genera
-------------------

.. autofunction:: pytuning.scales.create_euler_fokker_scale

Diatonic Scales
---------------

.. autofunction:: pytuning.scales.create_diatonic_scale

As another example of creating a diatonic scale, we can use the five-limit
constructors (which are defined in ``pytuning.constants``):

.. code:: python

  five_limit_constructors = [
      (sp.Rational(16,15), "s"),
      (sp.Rational(10,9),  "t"),
      (sp.Rational(9,8),   "T"),
  ]

to create *Ptolemy's Intense Diatonic Scale*:

.. code:: python

  from pytuning.constants import five_limit_constructors
  from pytuning.scales import create_diatonic_scale

  scale = create_diatonic_scale(five_limit_constructors,
    ["T", "t", "s", "T", "t", "T", "s"])

which gives us:

.. math::

  \left [ 1, \quad \frac{9}{8}, \quad \frac{5}{4}, \quad \frac{4}{3}, \quad
  \frac{3}{2}, \quad \frac{5}{3}, \quad \frac{15}{8}, \quad 2\right ]

Note that if every identifier is a single-character string, ``specification``
can also be passed in as a string. So this is equivalent:

.. code:: python

  from pytuning.constants import five_limit_constructors
  from pytuning.scales import create_diatonic_scale

  scale = create_diatonic_scale(five_limit_constructors, "TtsTtTs")
