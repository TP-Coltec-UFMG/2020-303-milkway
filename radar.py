import openal as oal
from struct import pack
from math import sin, pi
import time


def vai_bater(nave, asteroides):
    nLarg = nave.image.get_width() / 2  # metade da largura da nave
    nRec = nave.rect

    for a in asteroides:
        aLarg = a.image.get_width() / 2 # metade da largura do asteroide
        aRec = a.rect

        # se a direita do asteroide estiver em rota de colisao com a nave
        if (aRec.x + aLarg >= nRec.x - nLarg) and (aRec.x + aLarg <= nRec.x + nLarg):
            return True

        # se a esquerda do asteroide estiver em rota de colisao com a nave
        if (aRec.x - aLarg >= nRec.x - nLarg) and (aRec.x - aLarg <= nRec.x + nLarg):
            return True

    return False


def alarme(nave, som, asteroides=[], *args):
    for a in asteroides:
        reca = a.rect
        recn = nave.rect
        if vai_bater(nave, asteroides):
            dist = recn.y - reca.y
            if dist != 0:
                som.set_volume(10/dist)
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
