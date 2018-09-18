# A music note, comprised of the note value (A B C D E F G) and note octave (3 4 5 6)
class Note:
    def __init__(self, note, octave):
        self.note = note
        self.octave = octave

    def __eq__(self, other):
        return self.note == other.note and self.octave == other.octave

    def __str__(self):
        return str(self.note) + str(self.octave)
