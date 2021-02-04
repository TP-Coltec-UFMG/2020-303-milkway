import pygame
import openal as oal
import values


class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y, vida):
        pygame.sprite.Sprite.__init__(self)

        # variaveis de imagem
        self.image = pygame.image.load("assets/images/nave2 (1).png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        # variaveis de vida
        self.vidas_inicio = vida
        self.vidas_restantes = vida

        # define o listener
        self.listen = oal.oalGetListener()

    def update(self, surface):
        """
        Atualiza as variaveis da nave e desenha ela na tela
        """
        velocidade = 8

        # pegar movimentos do teclado
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= velocidade
        if key[pygame.K_RIGHT] and self.rect.right < values.screen_width:
            self.rect.x += velocidade

        # desenha vidas
        pygame.draw.rect(surface, values.VERMELHO, (20, 40, self.rect.width, 15))
        if self.vidas_restantes > 0:
            pygame.draw.rect(surface, values.VERDE, (20, 40, int(
                self.rect.width*(self.vidas_restantes/self.vidas_inicio)), 15))

        # mudando posicao do listener para se adequar a nave
        self.listen.set_position((self.rect.x, 0, self.rect.y/values.f))
