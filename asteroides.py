import pygame
import openal as oal
import openal.al as al
from random import randrange
import values

class Asteroides(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/asteroides.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # seleciona um arquivo aleatorio de audio
        self.source = oal.oalOpen(
            "assets/sounds/b"+str(randrange(400, 1100, 100))+".wav")
        self.source.set_looping(True)
        self.source.set_position((x, 0, y))
        self.source.play()

    def __del__(self):
        # quando for deletado essa funcao sera chamada
        self.stop_sound()
        del self.source

    def update(self):
        """
        Atualiza a posicao do asteroide e a fonte de som dele
        """
        self.rect.y += 2

        # atualizando fonte do som
        self.source.set_position((self.rect.x, 0, self.rect.y/values.f))
        self.source.update()

    def stop_sound(self):
        self.source.stop()
        # Limpar memória
        al.alDeleteSources(1, self.source.id)
