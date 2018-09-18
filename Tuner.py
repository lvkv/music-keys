import numpy as np
import pyaudio
import audioop
from keystrokes import *

NOTE_MIN = 48  # Lowest note (C3)
NOTE_MAX = 95  # Highest note (B6)
FSAMP = 22050  # Sampling frequency in Hz
FRAME_SIZE = 1024  # How many samples per frame?
FRAMES_PER_FFT = 2  # FFT (Fast fourier transform) takes average across how many frames?
SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT
FREQ_STEP = float(FSAMP) / SAMPLES_PER_FFT
VOLUME_THRESHOLD = 30  # Minimum volume to register input
A4 = 440.0  # A4 = 440 Hz
SEMITONE = 69
NOTES_IN_OCTAVE = 12.0
NOTE_NAMES = 'C C D D E F F G G A A B'.split()
WINDOW = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, SAMPLES_PER_FFT, False)))


def freq_to_number(f):
    return SEMITONE + NOTES_IN_OCTAVE * np.log2(f / A4)


def number_to_freq(n):
    return A4 * 2.0 ** ((n - SEMITONE) / NOTES_IN_OCTAVE)


def note_to_fftbin(n):
    return number_to_freq(n) / FREQ_STEP


def set_threshold(new_threshold):
    VOLUME_THRESHOLD = new_threshold
    print('The new volume threshold is',VOLUME_THRESHOLD,' db')


def run(mappings):
    imin = max(0, int(np.floor(note_to_fftbin(NOTE_MIN - 1))))
    imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(NOTE_MAX + 1))))

    # Allocate space to run an FFT.
    buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
    num_frames = 0

    # Initialize audio
    stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                    channels=1,
                                    rate=FSAMP,
                                    input=True,
                                    frames_per_buffer=FRAME_SIZE)

    stream.start_stream()

    while True:
        # Calculate volume
        rms = audioop.rms(stream.read(FRAME_SIZE), 2) // 100
        if rms < VOLUME_THRESHOLD:
            continue

        # Shift the buffer down and new data in
        buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
        buf[-FRAME_SIZE:] = np.fromstring(stream.read(FRAME_SIZE), np.int16)

        # Run the FFT on the windowed buffer
        fft = np.fft.rfft(buf * WINDOW)

        # Get frequency of maximum response in range
        freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP

        # Get note number and nearest note
        n = int(round(freq_to_number(freq)))

        # Console output once we have a full buffer
        num_frames += 1
        if num_frames >= FRAMES_PER_FFT:
            note_name = NOTE_NAMES[n % int(NOTES_IN_OCTAVE)] + str(n // int(NOTES_IN_OCTAVE) - 1)
            if note_name in mappings:
                press_key(mappings[note_name])
