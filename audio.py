import openal as oal
import time

testes = {
    400: "assets/sounds/b400.wav",
    700: "assets/sounds/b700.wav",
    1100: "assets/sounds/b1100.wav"
}


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


make_sounds([(2, 0, -5), (-4, 0, -7), (6, 0, -4)], [testes[400], testes[700], testes[1100]])
make_sounds([(2, 0, -3), (-4, 0, -5), (6, 0, -2)], [testes[400], testes[700], testes[1100]])
oal.oalQuit()
