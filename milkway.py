# Precisa baixar: pip install pygame-menu
import pygame
import pygame_menu
from random import randrange
from radar import generate_mono
import openal as oal

pygame.init()

# Som/Radar
pygame.mixer.init()
som_radar = generate_mono(440)
som = pygame.mixer.Sound(som_radar)
RADAREVENT = pygame.USEREVENT+1
pygame.time.set_timer(RADAREVENT, 750)  # 750 ms para cada apito

f = 0.7  # fator de divisao para tornar o som mais proximo

screen_width = 900
screen_height = 500
surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('MilkWay')

# carrega imagem de fundo
bg = pygame.image.load("assets/images/espaço.gif")

# definindo cores
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# fonte da letra
fonte = pygame.font.SysFont("arial", 20, True, False)


# coloca imagem de fundo na tela
def draw_bg():
    surface.blit(bg, (0, 0))
    texto_img = fonte.render("ESTABILIDADE DA NAVE", True, BRANCO)
    surface.blit(texto_img, (20, 15))


def radar(nave, asteroides=[], *args):
    for a in asteroides:
        if (a.rect.x-50 <= nave.rect.x) and (a.rect.x+50 >= nave.rect.x):
            som.play()


# Classe Nave principal
class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y, vida):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/naveEspacial.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vidas_inicio = vida
        self.vidas_restantes = vida
        self.listen = oal.oalGetListener()

    def update(self):
        # pegar movimentos do teclado
        velocidade = 8
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= velocidade
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += velocidade

        # desenha vidas
        pygame.draw.rect(surface, VERMELHO, (20, 40, self.rect.width, 15))
        if self.vidas_restantes > 0:
            pygame.draw.rect(surface, VERDE, (20, 40, int(
                self.rect.width*(self.vidas_restantes/self.vidas_inicio)), 15))

        # mudando posicao do listener para se adequar a nave
        self.listen.set_position((self.rect.x, 0, self.rect.y/f))


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

    def update(self):
        """
        Atualiza a posicao do asteroide e a fonte de som dele
        """
        self.rect.y += 2

        # atualizando fonte do som
        self.source.set_position((self.rect.x, 0, self.rect.y/f))
        self.source.update()

    def stop_sound(self):
        self.source.stop()
        # Limpar memória
        self.source.destroy()


grupo_naves = pygame.sprite.Group()
nave = Nave(int(screen_width/2), screen_height - 50, 5)
grupo_naves.add(nave)

grupo_asteroides = []
grupo_asteroides = pygame.sprite.Group()


def Game_Start():
    # fps do jogo
    clock = pygame.time.Clock()
    fps = 60

    # qtd de asteroides criados por vez
    qtd_asteroides = 4

    # controlador para sair
    run = True

    while run:

        # fps da tela
        clock.tick(fps)

        # desenha fundo
        draw_bg()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                oal.oalQuit()
                run = False
                pygame.quit()
                break
            if event.type == RADAREVENT:
                pass
                # radar(nave, grupo_asteroides)

        # Cria asteroides se não existem na tela
        if qtd_asteroides > 0:
            qtd_asteroides -= 1
            asteroide = Asteroides(randrange(screen_width - 8), randrange(1))
            grupo_asteroides.add(asteroide)

        for asteroide in grupo_asteroides:
            # +30 pro som demorar um poquinho pra ir embora
            if asteroide.rect.y > screen_height+30:
                asteroide.stop_sound()  # encerra o som do asteroide
                qtd_asteroides += 1
                asteroide.kill()
            elif pygame.sprite.spritecollide(asteroide, grupo_naves, False):
                nave.vidas_restantes -= 1
                asteroide.stop_sound()  # encerra o som do asteroide
                qtd_asteroides += 1
                asteroide.kill()
            else:
                asteroide.update()

        nave.update()
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
