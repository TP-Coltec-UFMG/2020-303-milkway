# Precisa baixar: pip install pygame-menu
import pygame
import pygame_menu
from random import randrange
from radar import generate_mono
import openal as oal
import values
from nave import Nave
from asteroides import Asteroides
# import openal.al as al

pygame.init()

# Som/Radar
pygame.mixer.init()
som_radar = generate_mono(440)
som = pygame.mixer.Sound(som_radar)
boom = oal.oalOpen("assets/sounds/bip2.ogg")
RADAREVENT = pygame.USEREVENT+1
pygame.time.set_timer(RADAREVENT, 750)  # 750 ms para cada apito


screen_width = values.screen_width
screen_height = values.screen_height
surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('MilkWay')

# carrega imagem de fundo
bg = pygame.image.load("assets/images/espaço.gif")

# fonte da letra
fonte = pygame.font.SysFont("arial", 20, True, False)


# coloca imagem de fundo na tela

def draw_bg():
    surface.blit(bg, (0, 0))
    texto_img = fonte.render("ESTABILIDADE DA NAVE", True, values.BRANCO)
    surface.blit(texto_img, (20, 15))

grupo_naves = pygame.sprite.Group()
nave = Nave(int(screen_width/2), screen_height - 50, 5)
grupo_naves.add(nave)

grupo_asteroides = []
grupo_asteroides = pygame.sprite.Group()


def Game_Start(blind_mode=False):
    # fps do jogo
    clock = pygame.time.Clock()
    fps = 60

    # qtd de asteroides criados por vez
    qtd_asteroides = 2

    # controlador para sair
    run = True

    while run:

        # fps da tela
        clock.tick(fps)

        # desenha fundo
        draw_bg()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for ast in grupo_asteroides:
                    ast.kill()
                    del ast
                run = False
                pygame.mixer.stop()
                # pygame.quit()
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
                # asteroide.stop_sound()  # encerra o som do asteroide
                qtd_asteroides += 1
                asteroide.kill()
                del asteroide
            elif pygame.sprite.spritecollide(asteroide, grupo_naves, False):
                boom.play()
                nave.vidas_restantes -= 1
                # asteroide.stop_sound()  # encerra o som do asteroide
                qtd_asteroides += 1
                asteroide.kill()
                del asteroide
            else:
                asteroide.update()

        nave.update(surface)
        grupo_naves.draw(surface)
        grupo_asteroides.draw(surface)
        if blind_mode:
            surface.fill((0, 0, 0))
        pygame.display.update()

    pygame.quit()


def Blind_Game_Start():
    Game_Start(True)


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
menu.add_button('Blind Mode', Blind_Game_Start)
menu.add_button('Sair', pygame_menu.events.EXIT)

menu.mainloop(surface)

pygame.quit()
oal.oalQuit()
