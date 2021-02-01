import openal as oal
from struct import pack
from math import sin, pi
import time

def alarme(nave, som, asteroides=[], *args):
    for a in asteroides:
        if (a.rect.x-50 <= nave.rect.x) and (a.rect.x+50 >= nave.rect.x) and (a.rect.y +300 > nave.rect.y):
            som.play()

def generate_mono(frequency):
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

    return waveData


def make_sounds(positions, sounds):
    """
    Recebe lista com as posicoes e lista com os sons a serem reproduzidos
    Reproduz os sons considerando suas respectivas posicoes
    """
    if not oal.oalGetInit():
        oal.oalInit()
    print(oal.oalGetInit())
    sources = []
    for position, sound in zip(positions, sounds):
        source = oal.oalOpen(sound)
        source.set_position(position)
        sources.append(source)
    for source in sources:
        source.play()
        time.sleep(0.2)
    some_running = True
    while some_running:
        some_running = False
        for source in sources:
            if source.get_state() == oal.AL_PLAYING:
                some_running = True
        time.sleep(0.1)
    oal.oalQuit()
