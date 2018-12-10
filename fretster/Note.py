from enum import Enum

# Constant strings for unicode sharp/flat
_SHARP = u'♯'
_FLAT = u'♭'

# Enum class to represent different intervals
class Interval(Enum):
    #TODO: God these are ugly
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

class ChordEnum(Enum):
    # Youre right, it did suck writing this out
    Maj = (Interval.ROOT, Interval.M3, Interval.P5)
    m = (Interval.ROOT, Interval.m3, Interval.P5)
    Aug = (Interval.ROOT, Interval.M3, Interval.aug5)
    Dim = (Interval.ROOT, Interval.m3, Interval.dim5)
    Sus4 = (Interval.ROOT, Interval.P4, Interval.P5)
    Sus2 = (Interval.ROOT, Interval.M2, Interval.P5)
    Maj7 = (Interval.ROOT, Interval.M3, Interval.P5, Interval.M7)
    Dom7 = (Interval.ROOT, Interval.M3, Interval.P5, Interval.M7)
    m7 = (Interval.ROOT, Interval.m3, Interval.P5, Interval.M7)
    HalfDim = (Interval.ROOT, Interval.m3, Interval.dim5, Interval.M7)
    Dim7 = (Interval.ROOT, Interval.m3, Interval.dim5, Interval.dim7)
    Sixth = (Interval.ROOT, Interval.M3, Interval.P5, Interval.M6)
    m6 = (Interval.ROOT, Interval.m3, Interval.P5, Interval.M6)
    Add9 = (Interval.ROOT, Interval.M3, Interval.P5, Interval.M9)
    Dom9 = (Interval.ROOT, Interval.M3, Interval.P5, Interval.M7, Interval.M9)
    Maj9 = (Interval.ROOT, Interval.M3, Interval.P5, Interval.M7, Interval.M9)
    m9 = (Interval.ROOT, Interval.m3, Interval.P5, Interval.M7, Interval.M9)
    SixNine = (Interval.ROOT, Interval.M3, Interval.P5, Interval.M6, Interval.M9)
    m11 = (Interval.ROOT, Interval.M3, Interval.P5, Interval.M7, Interval.P11)
    Dom13 = (Interval.ROOT, Interval.M3, Interval.P5, Interval.M7, Interval.M9, Interval.M13)
    Maj7aug11 = (Interval.ROOT, Interval.M3, Interval.aug11, Interval.M7)

    

class Chord:
    def __init__(self, root, chordType=ChordEnum.Maj):
            self.root = root
            self.chordType = chordType
            self.tones = [c.value + self.root for c in self.chordType]
    
    @classmethod
    def fromName(cls, string):
        noteStr, chordStr = string.split("_")
        return cls(Note[noteStr], ChordEnum[chordStr])

    def __add__(self, val):
        if isinstance(val, int) or isinstance(val,Interval):
            return Chord(self.root + val,[tone + val for tone in self.tones])
        
            
        else:
            raise TypeError(f"Addition is not supported for type {type(val)}")
        

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

#==========================================
# Enum Definitions
#==========================================
    BsC = Bs = C = 0
    CsDf = Cs = Df = 1
    D = 2
    DsEf = Ds = Ef = 3
    E_Ff = E = Ff = 4
    EsF = Es = F = 5
    FsGf = Fs = Gf = 6
    G = 7
    GsAf = Gs = Af = 8
    A = 9
    AsBf = As = Bf = 10
    B_Cf = B = Cf = 11
   
#==========================================
# Operator methods
#==========================================

    # Integer Addition. The parameter integer refers to the number of half-steps
    # above the note
    def __add__(self, val):
        if isinstance(val, int):
            return Note((self.value + val) % 12)
        elif isinstance(val, Interval):
            return Note((self.value + val.value) % 12)
        else:
            raise TypeError(f"Type {type(val)} is not supported for '+'")

    def __iadd__(self,val):
        if isinstance(val,int):
            return Note(self.value + val)
        elif isinstance(val, Interval):
            return Note(self.value + val.value)

        else:
            raise TypeError(f"Addition-Assignment not supported for type {type}")

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
    def __add__(self, val):
        if isinstance(val,int):
            note = self.note + val
            octave = self.octave + (self._note.value + val) // 12
            return Pitch(Note.C, 0) if octave < 0 else Pitch(note,octave)
        
        elif isinstance(val, Interval):
            note = self.note + val.value
            octave = self.octave + (self._note.value + val.value) // 12
            return Pitch(Note.C, 0) if octave < 0 else Pitch(note,octave)
        
        # Implement
        elif isinstance(val, Pitch):
            raise NotImplementedError

        elif isinstance(val, Note):
            return self + Pitch(val, self.octave)
        
        else:
            raise TypeError(f"Addition not supported for {type(val)}")

    def __iadd__(self,val):
        if isinstance(val, Interval):
            val = val.value
        if isinstance(val, int):
            octave = self.octave + (self._note.value + val) // 12
            if octave < 0:
                self.note = Note.C
                self.octave = 0
            else:
                self.note += val
                self.octave = octave
      


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


# Constants for standard tuning
_STANDARD_TUNING_NOTES = [Note.E, Note.A, Note.D, Note.G, Note.B, Note.E]
_STANDARD_TUNING_PITCHES = [Pitch(Note.E, 2), Pitch(Note.A, 2), Pitch(Note.D, 3), Pitch(Note.G, 3), Pitch(Note.B, 3),
               Pitch(Note.E, 4)]

# Gets the frets where a note can be played on the strings of a guitar. 
def notesOnStrings(note,nFrets=24, tuning=_STANDARD_TUNING_NOTES):
    return [(st, [i for i in range(nFrets) if st + i is note]) for st in tuning]

# Gets the frets where a note can be played on the strings of a guitar.
def pitchOnStrings(pitch, nFrets=24, tuning=_STANDARD_TUNING_PITCHES):
    return [(st,
             None if len([i for i in range(nFrets) if st + i == pitch]) is 0 else [i for i in range(nFrets) if st + i == pitch][
                 0]) for st in tuning]

x = Note.A
print(x)
x +=2
print(x)