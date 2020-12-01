import openal as oal
import time


def make_sounds(positions, sounds):
    """
    Recebe lista com as posicoes e lista com os sons a serem reproduzidos
    Reproduz os sons considerando suas respectivas posicoes
    """
    sources = []
    for position, sound in zip(positions, sounds):
        source = oal.oalOpen(sound)
        source.set_position(position)
        sources.append(source)
    for source in sources:
        source.play()
    time.sleep(3)
    oal.oalQuit()


# Por algum motivo so esse house_lo.ogg funciona o som 3d

make_sounds([(-2, 0, 0)], ["assets/house_lo.ogg"])
make_sounds([(2, 0, 0)], ["assets/house_lo.ogg"])
make_sounds([(-2, -2, -2)], ["assets/bip2.ogg"])
make_sounds([(2, 2, 2)], ["assets/bip2.ogg"])
# make_sounds([(0, 0, -1), (4, 0, 0)], ["assets/bip1.ogg", "assets/bip2.ogg"])
