# -*- coding: utf-8 -*-
"""
Created on Tue May 26 10:49:30 2015

@author: mark
"""

import sympy as sp

try:
    numbers = sp.numbers   # type:ignore
except AttributeError:
    numbers = sp.core.numbers

from pytuning.utilities import note_number_to_freq, ratio_to_cents


def create_timidity_tuning(scale, reference_note=60, reference_frequency=None):
    '''
    Create a Timidity++ tuning table

    :param scale: The scale to model (list of frequency ratios)
    :param reference_note: The MIDI number of the absolute frequency reference
    :param reference_frequency: The frequency of the reference note. If ``None``
        (the default) the frequency will be taken from the standard MIDI 12-EDO tuning
    :returns: A Timidity tuning table as a ``String``

    The default value of ``reference_note`` pegs
    the scale to to the standard concert tuning of middle C (A = 440Hz).

    The Timidity table is basically a list of integers for all defined
    MIDI note numbers, with each entry as 1000 times the note frequency

    As a somewhat detailed example, let's say that the user had a 12-EDO
    scale constructed, and wanted to pin the tonic note to
    the standard A440. The following will do this:

    .. code::

        from pytuning.scales import create_edo_scale
        from pytuning.tuning_tables import create_timidity_tuning

        scale = create_edo_scale(12)
        tuning_table = create_timidity_tuning(scale, reference_note=69)

    with the first part of the table given by:

    .. code::

        # Timidity tuning table created by pytuning,
        # call timidity with the -Z option to enable.
        # Note reference: 69; Freq reference: 440.000000 Hz
        8176
        8662
        9177
        9723
        10301
        10913
        11562
        12250
        12978

    To use the table, one starts Timidity with the **-Z** option, i.e:

    .. code::

        timidity -Z table.name -iA

    '''
    if reference_frequency is None:
        reference_frequency = note_number_to_freq(reference_note)

    output_string = '''# Timidity tuning table created by pytuning,
# call timidity with the -Z option to enable.
# Note reference: %d; Freq reference: %f Hz''' % (reference_note, reference_frequency)
    for note in range(128):
        output_string = output_string + '\n' + str(
            int(round(
                note_number_to_freq(
                    note, scale, reference_note=reference_note, reference_frequency=reference_frequency) * 1000.0))
        )
    return output_string


def create_em_tuning(scale, reference_note=60, reference_frequency=None):
    '''
        Create a Timidity++ tuning table

        :param scale: The scale to model (list of frequency ratios)
        :param reference_note: The MIDI number of the absolute frequency reference
        :param reference_frequency: The frequency of the reference note. If ``None``
            (the default) the frequency will be taken from the standard MIDI 12-EDO tuning
        :returns: An Emergent tuning table as a ``String``

        The default value of ``reference_note`` and ``reference_frequency`` pegs
        the scale to to the standard concert tuning of middle C (A = 440Hz).

    '''
    if reference_frequency is None:
        reference_frequency = note_number_to_freq(reference_note)

    output_string = '''# Emergent Tuning Table created by MCW
# Note reference: %d; Freq reference: %f Hz''' % (reference_note, reference_frequency)
    for note in range(128):
        output_string = output_string + '\n' + "set tuning ( " + str(note) + "    " + str(
            note_number_to_freq(note, scale, reference_note=reference_note,
                                reference_frequency=reference_frequency)
        ) + ")"
    return output_string


def create_fluidsynth_tuning(scale, reference_note=60, chan=[0], bank=0, prog=[0],
                             reference_frequency=None):
    '''
    Create a Fluidsynth tuning table

    :param scale: The scale to model (list of frequency ratios)
    :param reference_note: The MIDI number of the absolute frequency reference
    :param reference_frequency: The frequency of the reference note. If ``None``
        (the default) the frequency will be taken from the standard MIDI 12-EDO tuning
    :param chan: A list of channels for which to create the table
    :param bank: The bank for the tuning table
    :param prog: A list of program numbers for the tuning table
    :returns: A Fluidsynth tuning table as a ``String``

    The default value of ``reference_note`` pegs
    the scale to to the standard concert tuning of middle C (A = 440Hz).

    The Fluidsyny tuning model allows each channel, bank, and program
    to have a different tuning. Thus, if one, say, wants all programs
    to be tuned to the scale, the tuning table can get quite large.

    As a somewhat detailed example, let's say that the user had a 12-EDO
    scale constructed, and wanted to pin the tonic note to
    the standard A440. The following will do this:

    .. code::

        from pytuning.scales import create_edo_scale
        from pytuning.tuning_tables import create_timidity_tuning

        scale = create_edo_scale(12)
        tuning_table = create_fluidsynth_tuning(scale, prog=range(128), reference_note=69)

    with the first part of the table given by:

    .. code::

        # Fluidsynth Tuning Table created by pytuning
        # Note reference: 69; Freq reference: 440.000000 Hz
        tuning tuning000 0 0
        tune 0 0 0 0.000000
        tune 0 0 1 100.000000
        tune 0 0 2 200.000000
        tune 0 0 3 300.000000
        tune 0 0 4 400.000000
        tune 0 0 5 500.000000
        tune 0 0 6 600.000000
        tune 0 0 7 700.000000
        tune 0 0 8 800.000000
        tune 0 0 9 900.000000

    To use the table, one should start fluidsynth with the **-f** option:

    .. code::

        fluidsynth -f table.name


    '''

    # The fluidsynth tuning table apears to be in cents, based upon a standard 12-EDO scale,
    # 69 = 440.0 Thus we'll need to calculate this base freqency

    if reference_frequency is None:
        reference_frequency = note_number_to_freq(reference_note)

    base_freq = note_number_to_freq(0, None, reference_note=69,
                                    reference_frequency=440.0)
    output_string = '''# Fluidsynth Tuning Table created by pytuning
# Note reference: %d; Freq reference: %f Hz''' % (reference_note, reference_frequency)
    for program in prog:
        output_string = output_string + "\ntuning tuning%03d %d %d" % (program, bank, program)
        for note in range(128):
            freq = note_number_to_freq(
                note, scale, reference_note=reference_note, reference_frequency=reference_frequency)
            cents = ratio_to_cents(freq / base_freq) if ratio_to_cents(freq / base_freq) > 0.00001 else 0.0
            output_string = output_string + "\ntune %d %d %d %f" % (bank, program, note, cents)
    for channel in chan:
        for program in prog:
            output_string = output_string + "\nsettuning %d %d %d" % (channel, bank, program)
    return output_string


def create_scala_tuning(scale, name):
    '''
    Create a Scala scale file

    :param scale: The scale (list of frequency ratios)
    :param name: The name of the scale
    :returns: A Scala file as a ``String``

    The Scala file can be used to tune various things, most
    germane being Yoshimi. However, keep in mind that the Scala
    file does **not** include a base note or frequency, so for tuning
    purposes those data will need to be captured or input in
    some other way.

    As an example of use, the Scala file for the default Pythagorean
    tuning can be calculated thus:

    .. code::

        from pytuning.scales.pythagorean import create_pythagorean_scale
        from pytuning.tuning_tables import create_scala_tuning

        scale = create_pythagorean_scale()
        table = create_scala_tuning(scale,"Pythagorean Tuning")

    which yields:

    .. code::

        ! Scale produced by pytuning. For tuning yoshimi or zynaddsubfx,
        ! only include the portion below the final '!'
        !
        Pythagorean Tuning
        12
        !
        256/243
        9/8
        32/27
        81/64
        4/3
        1024/729
        3/2
        128/81
        27/16
        16/9
        243/128
        2/1

    Note that the Scala file uses exact ratios where possible, otherwise
    it will convert to a cent value. Thus the code:

    .. code::

        from pytuning.scales import create_edo_scale
        from pytuning.tuning_tables import create_scala_tuning

        scale = create_edo_scale(12)
        table = create_scala_tuning(scale,"12-TET Tuning")

    will produce:

    .. code::

        ! Scale produced by pytuning. For tuning yoshimi or zynaddsubfx,
        ! only include the portion below the final '!'
        12-TET Tuning
        12
        !
        100.00000
        200.00000
        300.00000
        400.00000
        500.00000
        600.00000
        700.00000
        800.00000
        900.00000
        1000.00000
        1100.00000
        2/1

    '''
    output = "! Scale produced by pytuning. For tuning yoshimi or zynaddsubfx,\n! only include the portion below the final '!'"
    output = output + "\n!"
    output = output + "\n%s" % name
    output = output + "\n%3d" % (len(scale) - 1)
    output = output + "\n!"
    for degree in scale[1:]:
        if isinstance(degree, numbers.Rational) and isinstance(sp.fraction(degree)[0], numbers.Integer) \
                and isinstance(sp.fraction(degree)[1], numbers.Integer):
            representation = "%s" % degree
        elif isinstance(degree, numbers.Integer) or isinstance(degree, numbers.One):
            representation = "%s/1" % degree
        else:
            representation = "%0.5f" % ratio_to_cents(degree)
        output = output + "\n%s" % representation
    return output


def create_csound_tuning(scale, reference_note=60, reference_frequency=None,
                         table_num=1):
    '''
    Create a CSound tuning table

    :param scale: The scale (list of frequency ratios)
    :param reference_note: The MIDI number of the absolute frequency reference
    :param reference_frequency: The frequency of the reference note. If ``None``
        (the default) the frequency will be taken from the standard MIDI 12-EDO tuning
    :param table_num: The **f** table number to use

    CSound has many ways of generating microtonalities. For ``pytuning``
    a table lookup keyed on MIDI note number is used.

    As an example of use, let's say that we want to use the 12-EDO
    scale with the tonic at A440:

    .. code::

        from pytuning.scales import create_edo_scale
        from pytuning.tuning_tables import create_timidity_tuning

        scale = create_edo_scale(12)
        table = create_csound_tuning(scale, reference_note=69)

    This will produce the following output, which can be included in the
    CSound score file::

        f1 0 256 -2     8.17580     8.66196     9.17702     9.72272    10.30086    10.91338    11.56233    12.24986 \\
                       12.97827    13.75000    14.56762    15.43385    16.35160    17.32391    18.35405    19.44544 \\
                       20.60172    21.82676    23.12465    24.49971    25.95654    27.50000    29.13524    30.86771 \\
                       32.70320    34.64783    36.70810    38.89087    41.20344    43.65353    46.24930    48.99943 \\
                       51.91309    55.00000    58.27047    61.73541    65.40639    69.29566    73.41619    77.78175 \\
                       82.40689    87.30706    92.49861    97.99886   103.82617   110.00000   116.54094   123.47083 \\
                      130.81278   138.59132   146.83238   155.56349   164.81378   174.61412   184.99721   195.99772 \\
                      207.65235   220.00000   233.08188   246.94165   261.62557   277.18263   293.66477   311.12698 \\
                      329.62756   349.22823   369.99442   391.99544   415.30470   440.00000   466.16376   493.88330 \\
                      523.25113   554.36526   587.32954   622.25397   659.25511   698.45646   739.98885   783.99087 \\
                      830.60940   880.00000   932.32752   987.76660  1046.50226  1108.73052  1174.65907  1244.50793 \\
                     1318.51023  1396.91293  1479.97769  1567.98174  1661.21879  1760.00000  1864.65505  1975.53321 \\
                     2093.00452  2217.46105  2349.31814  2489.01587  2637.02046  2793.82585  2959.95538  3135.96349 \\
                     3322.43758  3520.00000  3729.31009  3951.06641  4186.00904  4434.92210  4698.63629  4978.03174 \\
                     5274.04091  5587.65170  5919.91076  6271.92698  6644.87516  7040.00000  7458.62018  7902.13282 \\
                     8372.01809  8869.84419  9397.27257  9956.06348 10548.08182 11175.30341 11839.82153 12543.85395

    '''
    if reference_frequency is None:
        reference_frequency = note_number_to_freq(reference_note)

    output_string = ""
    entries_per_line = 8
    line = "f%d 0 256 -2 " % table_num
    index = 1
    for note in range(128):
        freq = note_number_to_freq(
            note, scale, reference_note=reference_note, reference_frequency=reference_frequency)
        representation = "%11.5f" % freq
        line = line + representation + " "
        if index % entries_per_line == 0:
            line = line + "\\\n"
            output_string = output_string + line
            line = "            "
        index += 1
    output_string = output_string + line
    output_string = output_string.strip()
    if output_string[-1] == "\\":
        output_string = output_string[:-2]

    return output_string.strip() + "\n"
