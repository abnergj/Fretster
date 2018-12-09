from enum import Enum

# Constant strings for unicode sharp/flat
_SHARP = u'♯'
_FLAT = u'♭'


class Interval(Enum):
    ROOT = P1 = d2 = dim2 = 0
    min2 = m2 = A1 = aug1 = 1
    maj2 = M2 = d3 = dim3 = 2
    min3 = m3 = A2 = aug2 = 3
    maj3 = M3 = d4 = dim4 = 4
    perf4 = P4 = A3 = aug3 = 5
    dim5 = d5 = A4 = aug4 = 6
    perf5 = P5 = d6 = dim6 = 7
    min6 = m6 = A5 = aug5 = 8
    maj6 = M6 = d7 = dim7 = 9
    min7 = m7 = A6 = aug6 = 10
    maj7 = M7 = d8 = dim8 = 11
    octave = perf8 = P8 = A7 = aug7 = d9 = dim9 = 12
    min9 = m9 = A8 = aug8 = 13
    maj9 = M9 = d10 = dim10 = 14
    min10 = m10 = A9 = aug9 = 15
    maj10 = M10 = d11 = dim11 = 16
    perf11 = P11 = A10 = aug10 = 17
    dim12 = d12 = A11 = aug11 = 18
    perf12 = P12 = d13 = dim13 = 19
    min13 = m13 = A12 = aug12 = 20
    maj13 = M13 = d14 = dim14 = 21
    min14 = m14 = A13 = aug13 = 22
    maj14 = M14 = d15 = dim15 = 23
    perf15 = doctave = A14 = aug14 = 24


# Base class which adds functionality to Note
class _NoteAliaser(Enum):

    # Returns a string representation of the Note with
    # the given accidental

    # Sharp
    def asSharp(self):
        if len(self.name) == 1 or self.name[1] == '_':
            return self.name[0]
        else:
            return self.name[0] + _SHARP

    # Flat
    def asFlat(self):
        if len(self.name) == 1 or self.name[1] == '_':
            return self.name[0]
        else:
            return self.name[2] + _FLAT

    # Natural
    def asNat(self):
        if len(self.name) == 1 or self.name[1] == '_':
            return self.name[0]
        elif len(self.name) == 3:
            return self.name[-1]
        else:
            return self.name


# Enum type defining Notes. Does not take into account
# octaves. Note.A + 12 == Note.A
class Note(_NoteAliaser):
    A = 0
    AsBf = As = Bf = 1
    B_Cf = B = Cf = 2
    BsC = Bs = C = 3
    CsDf = Cs = Df = 4
    D = 5
    DsEf = Ds = Ef = 6
    E_Ff = E = Ff = 7
    EsF = Es = F = 8
    FsGf = Fs = Gf = 9
    G = 10
    GsAf = Gs = Af = 11

    # Integer Addition. The parameter integer refers to the number of half-steps
    # above the note
    def __add__(self, val):

        if isinstance(val, int):
            return Note((self.value + val) % 12)
        elif isinstance(val, Interval):
            return Note((self.value + val.value) % 12)
        else:
            raise TypeError(f"Type {type(val)} is not supported for '+'")

    # TODO: Impliment case for Note - Note = Interval
    # Integer Subtraction
    def __sub__(self, integer):
        return self if not isinstance(integer, int) else Note((self.value - integer) % 12)

    # String representation of the Note. Differs from the _NoteAnalyzer functions because
    # it doesn't prefer sharps or flats (A♯ returned as A♯\B♭) but does prefer naturals
    # (F♭ returned as E)
    def __str__(self):
        repSF = lambda st: st.replace('s', _SHARP).replace('f', _FLAT).replace('_', "")
        if len(self.name) == 1:
            return self.name
        else:
            return '/'.join([repSF(self.name[0:2]), repSF(self.name[2:])])

# Class to keep track of Note and octave along with other useful methods
class Pitch:
    _SHARP_FLAT = {-1: 'flat', 0: 'nat', 'sharp': 1}
    _NOTE_NAMES = [name for name, _ in Note.__members__.items()]

    @staticmethod
    def getNoteNames():
        return Pitch._NOTE_NAMES

    # TODO: Implement
    @staticmethod
    def getFrequency(note, octave):
        return 0.0

    def __init__(self, note, octave):
        self._note = note
        self._octave = octave
        self._freq = Pitch.getFrequency(note, octave)

    # Note, Freq, Octave are all properties in order to validate assignments
    @property
    def note(self):
        return self._note

    # Has to be a Note object
    @note.setter
    def note(self, value):
        if self._note == value:
            return
        elif not isinstance(value, Note):
            raise TypeError("Member variable 'note' must have type 'Note'")
        else:
            self._note = value
            self._freq = Pitch.getFrequency(self._note, self._octave)

    @property
    def octave(self):
        return self._octave

    # Can't be negative
    @octave.setter
    def octave(self, value):
        if value == self._octave:
            return
        elif not isinstance(value, int):
            raise TypeError("Member variable 'octave' must have type 'int'")
        elif value < 0:
            raise ValueError("Member variable 'octave' must be non-negative")
        else:
            self._octave = value
            self._freq = Pitch.getFrequency(self._note, self._octave)

    @property
    def freq(self):
        return self._freq

    # Ignores any attempts to change it. Raise Exception?
    @freq.setter
    def freq(self, value):
        pass


#==========================================
#   Operator Methods
#==========================================

    #TODO: Add implementation for adding intervals
    def __add__(self, integer):
        if not isinstance(integer, int):
            raise TypeError("Operator '+' uses type 'int' and type 'Pitch'")
        self._note = self.note + integer
        self._octave = (self._note + integer) // 12 + self.octave

        # Bounded below by A0. May change this later
        if self._octave < 0:
            self.note = Note.A
            self.octave = 0

    def __sub__(self, integer):
        return self + -integer

    def __str__(self):
        return str(self.note) + str(self.octave)

    def __eq__(self, other):
        return other.octave == self.octave and other.note == self.note

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return self.note + self.octave * 12 < other.note + other.octave * 12

    def __ge__(self, other):
        return self.note + self.octave * 12 <= other.note + other.octave * 12

    def __lt__(self, other):
        return other.note + other.octave * 12 < self.note + self.octave * 12

    def __le__(self, other):
        return other.note + other.octave * 12 <= self.note + self.octave * 12


def notesOnStrings(note):
    strings = [Note.E, Note.A, Note.D, Note.G, Note.B, Note.E]
    return [(st, [i for i in range(24) if st + i is note]) for st in strings]


# TODO: Create a constant list for standard tuning
def pitchOnStrings(pitch):
    strings = [Pitch(Note.E, 2), Pitch(Note.A, 2), Pitch(Note.D, 3), Pitch(Note.G, 3), Pitch(Note.B, 3),
               Pitch(Note.E, 4)]
    return [(st,
             None if len([i for i in range(24) if st + i == pitch]) is 0 else [i for i in range(24) if st + i == pitch][
                 0]) for st in strings]
