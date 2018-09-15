import numpy as np
import pyaudio
import audioop
import win32api
import win32con
import time
import const

NOTE_MIN = 48  # Lowest note (C3)
NOTE_MAX = 95  # Highest note (B6)
FSAMP = 22050  # Sampling frequency in Hz
FRAME_SIZE = 1024  # How many samples per frame?
FRAMES_PER_FFT = 2  # FFT (Fast fourier transform) takes average across how many frames?
VK_CODE = const.VK_CODE

SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT
FREQ_STEP = float(FSAMP) / SAMPLES_PER_FFT
volume_threshold = 30  # Minimum volume to register input

A4 = 440.0
SEMITONE = 69
NOTES_IN_OCTAVE = 12.0

NOTE_NAMES = 'C C D D E F F G G A A B'.split()


def freq_to_number(f): return SEMITONE + NOTES_IN_OCTAVE * np.log2(f / A4)


def number_to_freq(n): return A4 * 2.0 ** ((n - SEMITONE) / NOTES_IN_OCTAVE)


def note_to_fftbin(n): return number_to_freq(n) / FREQ_STEP


window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, SAMPLES_PER_FFT, False)))


def set_threshold(new_threshold):
    volume_threshold = new_threshold
    print('The new volume threshold is',volume_threshold,' db')

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

        if rms < volume_threshold:
            continue

        # Shift the buffer down and new data in
        buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
        buf[-FRAME_SIZE:] = np.fromstring(stream.read(FRAME_SIZE), np.int16)

        # Run the FFT on the windowed buffer
        fft = np.fft.rfft(buf * window)

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
                # print('volume: {:3d} note: {:>3s}'.format(rms, NOTE_NAMES[n % 12] + str(n // 12 - 1)))


def press_key(key):
    win32api.keybd_event(VK_CODE[key], 0, 0, 0)
    time.sleep(.05)
    win32api.keybd_event(VK_CODE[key], 0, win32con.KEYEVENTF_KEYUP, 0)
