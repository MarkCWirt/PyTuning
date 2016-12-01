Metric Functions
================

A **metric function** is a function that takes a scale as input and
returns a calculated value. As mentioned in :doc:`basic`, it returns
a Python ``dict`` with the metric name as the key, and the metric value
as the value.

The currently defined metrics all estimate the consonance or dissonance of
a scale.


sum_p_q()
---------

.. autofunction:: pytuning.metrics.sum_p_q

sum_distinct_intervals()
------------------------

.. autofunction:: pytuning.metrics.sum_distinct_intervals

metric_3()
----------

.. autofunction:: pytuning.metrics.metric_3

sum_p_q_for_all_intervals()
---------------------------

.. autofunction:: pytuning.metrics.sum_p_q_for_all_intervals

sum_q_for_all_intervals()
-------------------------

.. autofunction:: pytuning.metrics.sum_q_for_all_intervals

All Metrics
-----------

There is also a function that calculates all defined metrics for a
scale.

.. autofunction:: pytuning.metrics.all_metrics
