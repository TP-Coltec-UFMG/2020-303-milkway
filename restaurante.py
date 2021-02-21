import pygame

class Restaurante(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # lista de imagens para asteroide
        self.image = pygame.image.load("assets/images/restaurante.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
