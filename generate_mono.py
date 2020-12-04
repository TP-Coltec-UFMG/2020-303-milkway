from struct import pack
from math import sin, pi
import wave
from os.path import abspath


def generate_mono(frequency, filename):
    # create a bytestring containing "short" (2-byte) sine values
    SAMPLE_RATE = 44100
    waveData = b''
    maxVol = 2**15-1.0
    frequencyHz = frequency
    fileLengthSeconds = 1
    for i in range(0, SAMPLE_RATE * fileLengthSeconds):
        pcmValue = sin(i*frequencyHz/SAMPLE_RATE * pi * 2)
        pcmValue = int(maxVol*pcmValue)
        waveData += pack('h', pcmValue)

    # save the bytestring as a wave file
    outputFileName = filename
    wv = wave.open(outputFileName, 'w')
    wv.setparams((1, 2, SAMPLE_RATE, 0, 'NONE', 'not compressed'))
    wv.writeframes(waveData)
    wv.close()
    print(f"saved {abspath(outputFileName)}")


def generate_files():
    generate_mono(400, "assets/b400.wav")
    generate_mono(500, "assets/b500.wav")
    generate_mono(600, "assets/b600.wav")
    generate_mono(700, "assets/b700.wav")
    generate_mono(800, "assets/b800.wav")
    generate_mono(900, "assets/b900.wav")
    generate_mono(1000, "assets/b1000.wav")
    generate_mono(1100, "assets/b1100.wav")
