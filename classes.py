"""
Testando uma classe para gifs, nao precisa ser implementada
"""

import pygame

class Gif:
    def __init__(self, imagens, tempo = 10):
        self.imagens = imagens
        self.tempo = tempo
        self.imagem = 0
        self.contador = 0

    def update(self):
        self.contador += 1
        if self.contador == self.tempo:
            self.contador = 0
            self.imagem = self.proxima_imagem()

    def proxima_imagem(self):
        imagem = self.imagem + 1
        if imagem == len(self.imagens):
            imagem = 0
        return imagem

    def desenha(self, tela):
        tela.blit(self.imagens[self.imagem], (0, 0))

pygame.init()
surface = pygame.display.set_mode((900, 500))
imagens = []
imagens.append(pygame.image.load("assets/images/g1.png"))
imagens.append(pygame.image.load("assets/images/g2.png"))
imagens.append(pygame.image.load("assets/images/g3.png"))
imagens.append(pygame.image.load("assets/images/g4.png"))

gif = Gif(imagens, 100)

run = True

while run:
    gif.update()
    gif.desenha(surface)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
