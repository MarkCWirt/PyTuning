Number Theory
=============

While this part of the package isn't particularly fleshed out yet, there are
a few number-theoretic functions for the analysis of scales.


Odd Limits
----------

PyTuning contains functions for finding the `odd Limit
<https://en.wikipedia.org/wiki/Limit_(music)#Odd_limit>`__ for both intervals
and scales.

We can define and interval -- say, :math:`\frac{45}{32}`, and find its odd-limit
with the following:

.. code:: python

  from pytuning.number_theory import odd_limit

  interval = sp.Rational(45,32)
  limit = odd_limit(interval)

which yields and answer of 45.

One can also find the odd limit of an entire scale with the ``find_odd_limit_for_scale()``
function:

.. code::

  from pytuning.scales import create_euler_fokker_scale
  from pytuning.number_theory import find_odd_limit_for_scale

  scale = create_euler_fokker_scale([3,5],[3,1])
  limit = find_odd_limit_for_scale(scale)

which yields 135. (Examining the scale:

.. math::

  \left [ 1, \quad \frac{135}{128}, \quad \frac{9}{8}, \quad \frac{5}{4},
  \quad \frac{45}{32}, \quad \frac{3}{2}, \quad \frac{27}{16},
  \quad \frac{15}{8}, \quad 2\right ]

you will see that this is the largest odd number, and is found in
the second degree.)

.. autofunction:: pytuning.number_theory.odd_limit

.. autofunction:: pytuning.number_theory.find_odd_limit_for_scale

Prime Limits
------------

One can also compute `prime limits <https://en.wikipedia.org/wiki/Limit_(music)#Prime_limit>`__
for both scales and intervals. Extending the above example, one would assume that the
Euler-Fokker scale would have a prime-limit of 5, since that's the highest prime used
in the generation, and in fact:

.. code:: python

  from pytuning.scales import create_euler_fokker_scale
  from pytuning.number_theory import find_prime_limit_for_scale

  scale = create_euler_fokker_scale([3,5],[3,1])
  limit = find_prime_limit_for_scale(scale)

will return 5 as the limit.

.. autofunction:: pytuning.number_theory.prime_limit

.. autofunction:: pytuning.number_theory.find_prime_limit_for_scale

Prime Factorization of Degrees
------------------------------

PyTuning has functions for breaking a ratio down into prime factors, and
the inverse of reassembling them.

.. autofunction:: pytuning.number_theory.prime_factor_ratio

.. autofunction:: pytuning.number_theory.create_ratio_from_primes

