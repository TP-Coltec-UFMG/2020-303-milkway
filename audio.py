import openal as oal
import time


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
    # oal.oalQuit()


make_sounds([(2, 0, -5), (-4, 0, -7), (6, 0, -4)], ["assets/b400.wav", "assets/b700.wav", "assets/b1100.wav"])
make_sounds([(2, 0, -3), (-4, 0, -5), (6, 0, -2)], ["assets/b400.wav", "assets/b700.wav", "assets/b1100.wav"])
oal.oalQuit()
