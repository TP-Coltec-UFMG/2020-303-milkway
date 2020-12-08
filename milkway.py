# Precisa baixar: pip install pygame-menu
import pygame
import pygame_menu
from pygame.locals import *
from random import randrange

pygame.init()
screen_width = 900
screen_height = 500
surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('MilkWay')

# carrega imagem de fundo
bg = pygame.image.load("assets/images/espaço.gif")

# definindo cores
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)


# coloca imagem de fundo na tela
def draw_bg():
    surface.blit(bg, (0, 0))


# Classe Nave principal
class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y, vida):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/naveEspacial.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vidas_inicio = vida
        self.vidas_restantes = vida

    def movimento(self):
        # pegar movimentos do teclado
        velocidade = 8
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= velocidade
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += velocidade

        # pintar vidas
        # coração
        pygame.draw.circle(surface, VERMELHO, (20, 20), 5, 0)
        pygame.draw.circle(surface, VERMELHO, (30, 20), 5, 0)
        pygame.draw.polygon(surface, VERMELHO,
                            ((14, 20), (25, 32), (35, 20)), 0)


class Asteroides(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/asteroides.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 4


grupo_naves = pygame.sprite.Group()
nave = Nave(int(screen_width/2), screen_height - 50, 3)
grupo_naves.add(nave)

grupo_asteroides = []
grupo_asteroides = pygame.sprite.Group()


def Game_Start():
    # fps do jogo
    clock = pygame.time.Clock()
    fps = 60

    # qtd de asteroides criados por vez
    qtd_asteroides = 4

    rum = True
    while True:

        # fps da tela
        clock.tick(fps)

        # desenha fundo
        draw_bg()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                rum = False
                break

        # Cria asteroides se não existem na tela
        if qtd_asteroides > 0:
            qtd_asteroides -= 1
            asteroide = Asteroides(randrange(screen_width - 8), randrange(1))
            grupo_asteroides.add(asteroide)

        for asteroide in grupo_asteroides:
            asteroide.update()
            if asteroide.rect.y > screen_width:
                grupo_asteroides.remove(asteroide)
                qtd_asteroides += 1

        nave.movimento()
        grupo_naves.draw(surface)
        grupo_asteroides.draw(surface)
        pygame.display.update()

    pygame.quit()


# Carrega imagem de fundo do Menu
myimage = pygame_menu.baseimage.BaseImage(
    image_path="assets/images/espaço.gif",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
)

# Define a fonte do texto do Menu
font = pygame_menu.font.FONT_8BIT

# Cria a Theme do Menu
mytheme = pygame_menu.themes.Theme(
    title_background_color=(0, 0, 0),
    background_color=myimage,
    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
    widget_font=font,
    title_font=font,
    title_offset=(300, 100),
)

# Coloca o menu na Tela
menu = pygame_menu.Menu(screen_height, screen_width, 'MilkWay', theme=mytheme)
menu.add_button('Jogar', Game_Start)
menu.add_button('Instrucoes', pygame_menu.events.EXIT)
menu.add_button('Blind Mode', pygame_menu.events.EXIT)
menu.add_button('Sair', pygame_menu.events.EXIT)

menu.mainloop(surface)
