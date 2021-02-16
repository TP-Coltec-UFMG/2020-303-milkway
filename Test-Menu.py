import pygame
import gif
import milkwaymenu


def do_nothing():
    pass

pygame.init()
surface = pygame.display.set_mode((900, 500))
imagens = []
imagens.append(pygame.image.load("assets/images/g1.png"))
imagens.append(pygame.image.load("assets/images/g2.png"))
imagens.append(pygame.image.load("assets/images/g3.png"))
imagens.append(pygame.image.load("assets/images/g4.png"))

gif = gif.Gif(imagens)

options = [("Do nothing", do_nothing), ("Sair", exit)]
print("options foram criadas")
menu = milkwaymenu.Menu(options, gif, surface)

menu.loop()
