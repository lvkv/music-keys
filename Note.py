class Note:
    def __init__(self, note, octave):
        self.note = note
        self.octave = octave

    def __eq__(self, other):
        return self.note == other.note and self.octave == other.octave

    def __str__(self):
        return self.note + self.octave
