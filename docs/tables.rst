Tuning Tables
=============

A **tuning table** is a text representation of a scale that can be interpreted
by an external program. This is usually used to tune a synthesizer or other
sound source so that the scale can be used in a musical composition.

Some tuning tables -- such as that used by Scala -- describe the scale in
absolute terms, but most need to have a reference defined so that the scale
degrees can be mapped to a frequency. For this purpose the PyTuning package
has adopted the MIDI standard for note numbers and frequencies.

====== ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===
Octave   C   C#    D   D#    E    F   F#    G   G#    A   A#    B
====== ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===
-2       0    1    2    3    4    5    6    7    8    9   10   11
-1      12   13   14   15   16   17   18   19   20   21   22   23
 0      24   25   26   27   28   29   30   31   32   33   34   35
 1      36   37   38   39   40   41   42   43   44   45   46   47
 2      48   49   50   51   52   53   54   55   56   57   58   59
 3      60   61   62   63   64   65   66   67   68   69   70   71
 4      72   73   74   75   76   77   78   79   80   81   82   83
 5      84   85   86   87   88   89   90   91   92   93   94   95
 6      96   97   98   99  100  101  102  103  104  105  106  107
 7     108  109  110  111  112  113  114  115  116  117  118  119
 8     120  121  122  123  124  125  126  127
====== ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===  ===

So, for example, note number 69 corresponds to middle A, whereas 60
corresponds to middle C. The frequency standard is 12-EDO, and the note
69 is pegged to 440 Hz. Thus if you passed ``69`` as the reference note,
the 69'th entry in the table would be 440 Hz and this would correspond to the
first degree of the scale. ``60`` would cause the first degree of the scale
to be assigned to that note number (with a corresponding frequency of
about 261.6 Hz). The `timidity <http://timidity.sourceforge.net/>`__ soft synth
is an example of a synthesizer that needs this reference note and frequency.

In general the table will need to be output to disk so that it can read
by the program. This can be done with something like:

.. code:: python

  from pytuning.tuning_tables import create_timidity_tuning
  from pytuning.scales import create_euler_fokker_scale

  reference_note = 60
  scale = create_euler_fokker_scale([3,5],[3,1])

  tuning = create_timidity_tuning(scale, reference_note=reference_note)

  with open("timidity.table", "w") as table:
      table.write(tuning)

This will cause the generated scale:

.. math::

  \left [ 1, \quad \frac{135}{128}, \quad \frac{9}{8}, \quad \frac{5}{4},
  \quad \frac{45}{32}, \quad \frac{3}{2}, \quad \frac{27}{16},
  \quad \frac{15}{8}, \quad 2\right ]

to be written to a disk file, ``timidity.table``, which can be understood
by timidity::

  timidity -Z timidity.table score.mid

Timidity
--------

.. autofunction:: pytuning.tuning_tables.create_timidity_tuning

Scala
-----

The Scala tuning table can be used with the `Scala package
<http://www.huygens-fokker.org/scala/>`__, but it can also
be used to tune the soft synth `Zynaddsubfx <http://zynaddsubfx.sourceforge.net/>`__,
as well as its derivative `Youshimi <https://sourceforge.net/projects/yoshimi/>`__.
With the soft synths you will need to explicitly set the reference note and
frequency in the scale GUI.

.. autofunction:: pytuning.tuning_tables.create_scala_tuning

Fluidsynth
----------

.. autofunction:: pytuning.tuning_tables.create_fluidsynth_tuning

Csound
------

For use in `Csound <http://csound.github.io/>`__ PyTuning will generate a
table of frequencies that can be used as a table lookup, mapped to MIDI note
number. As mentioned in the basic concepts, the easiest way to use this
is via the ``table`` opcode::

  inote     init          p4
  iveloc    init          p5
  ifreq     table         inote, 1
  a1        oscil         iveloc, ifreq, 2
            outs          a1, a1

.. autofunction:: pytuning.tuning_tables.create_csound_tuning
