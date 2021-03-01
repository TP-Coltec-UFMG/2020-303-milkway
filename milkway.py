import pygame
import pygame_menu
from random import randrange
from radar import generate_mono, alarme
import openal as oal
import pyttsx3
import values
from nave import Nave
from asteroides import Asteroides
from restaurante import Restaurante

pygame.init()

# Som/Radar
pygame.mixer.init()
som_radar = generate_mono(440)
som = pygame.mixer.Sound(som_radar)
som.set_volume(0.1)
RADAREVENT = pygame.USEREVENT+1
pygame.time.set_timer(RADAREVENT, 750)  # 750 ms para cada apito

# som da explosao
boom = oal.oalOpen("assets/sounds/bip2.wav")
# som do inicio
inicio = pygame.mixer.Sound("assets/sounds/historia.mp3")
# som das instrucoes
instrucoes = pygame.mixer.Sound("assets/sounds/instrucoes.mp3")
# som do jogo ganho
ganhou = pygame.mixer.Sound("assets/sounds/ganhou.mp3")

# criando objeto que faz a voz
engine = pyttsx3.init()


# Narrador dos botões
def speakButton(widget, menu):
    """
    Recebe widget e menu. Uma voz diz o que esta escrito no widget
    """
    if menu.get_selected_widget() == widget:
        # Contador pra esperar o botão renderizar antes de falar
        itera = menu.get_attribute("iter", 0)
        # Botão selecionado antes do atual
        lBtn = menu.get_attribute("lastButton")
        if lBtn != widget:
            menu.set_attribute("lastButton", widget)
            itera = 0

        if itera > 3:
            texto = widget.get_title()
            engine.say(texto)
            engine.runAndWait()
            itera = -1  # Não falar dnv até mudar de botão

        if itera == -1:
            somar = 0
        else:
            somar = 1
        menu.set_attribute("iter", itera + somar)


# tela do pygame
screen_width = values.screen_width
screen_height = values.screen_height
surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('MilkWay')
pygame.display.set_icon(pygame.image.load("assets/images/naveEspacial4.png"))

# carrega imagem de fundo
bg = pygame.image.load("assets/images/espaço.gif")

# fonte da letra
fonte = pygame.font.SysFont("arial", 20, True, False)


def draw_bg():
    """
    Coloca imagem de fundo na tela
    """
    surface.blit(bg, (0, 0))


def draw_life():
    """
    Exibe a vida da nave
    """
    texto_img = fonte.render("ESTABILIDADE DA NAVE", True, values.BRANCO)
    surface.blit(texto_img, (20, 15))


# grupo de naves
grupo_naves = pygame.sprite.Group()
nave = Nave(int(screen_width/2), screen_height - 50, 5)
grupo_naves.add(nave)

# grupo de asteroides
grupo_asteroides = pygame.sprite.Group()

# grupo de restaurantes
restaurant = pygame.sprite.Group()


def ganhar_jogo(restaurante, blind_mode):
    ganhou.play()
    # fps do jogo
    clock = pygame.time.Clock()
    fps = 60

    # controlador para sair
    run = True

    while run:

        # fps da tela
        clock.tick(fps)

        # desenha fundo
        draw_bg()

        # desenha vida
        draw_life()

        restaurant.draw(surface)
        if restaurante.rect.y < 100:
            restaurante.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # se a pessoa aperta enter volta para o main menu
                if event.key == pygame.K_RETURN:
                    pygame.mixer.stop()
                    restaurante.kill()
                    main_menu()

        # atualiza a nave
        nave.update(surface)

        # blind_mode exibe apenas a nave em um fundo preto
        if blind_mode:
            surface.fill(values.PRETO)

        grupo_naves.draw(surface)
        pygame.display.update()


def game_start(blind_mode=False):
    """
    Funcao que comeca o jogo
    """

    nave.vidas_restantes = 5
    # fps do jogo
    clock = pygame.time.Clock()
    fps = 60

    # qtd de asteroides criados por vez
    qtd_asteroides = 2

    # pontuação do jogo
    score = 0

    # cria o restaurante
    restaurante = Restaurante(int(screen_width/2), -150)
    restaurant.add(restaurante)

    # controlador para sair
    run = True

    while run:

        # fps da tela
        clock.tick(fps)

        # desenha fundo
        draw_bg()

        for event in pygame.event.get():
            # se a pessoa sair encerra o jogo
            if event.type == pygame.QUIT:
                for ast in grupo_asteroides:
                    ast.kill()
                    ast.stop_sound()
                run = False
                pygame.mixer.stop()
                # pygame.quit()
                break
            # se passou determinado tempo chama funcao alarme
            if event.type == RADAREVENT:
                alarme(nave, som, grupo_asteroides)

        # Cria asteroides se a quantidade for menor que a esperada
        if qtd_asteroides > 0:
            qtd_asteroides -= 1
            asteroide = Asteroides(randrange(screen_width - 8), -100)
            grupo_asteroides.add(asteroide)

        # ganhar o jogo
        if score >= 20:
            for ast in grupo_asteroides:
                ast.kill()
                ast.stop_sound()
            pygame.mixer.stop()
            ganhar_jogo(restaurante, blind_mode)
            #restaurant.draw(surface)
            #if restaurante.rect.y < 100:
            #    restaurante.update()

            #if event.type == pygame.KEYDOWN:
            #    # se a pessoa aperta enter volta para o main menu
            #    if event.key == pygame.K_RETURN:
            #        restaurante.kill()
            #        main_menu()


        # destroi asteroides que sairam da tela ou colidiram
        for asteroide in grupo_asteroides:

            # se saiu da tela
            if asteroide.rect.y > screen_height+30:
                qtd_asteroides += 1
                score += 1
                asteroide.kill()
                asteroide.stop_sound()

            # se colidiu
            elif pygame.sprite.spritecollide(asteroide, grupo_naves, False):
                boom.play()
                nave.vidas_restantes -= 1   # reduz a vida da nave
                qtd_asteroides += 1
                asteroide.kill()
                asteroide.stop_sound()

                # Diz a quantidade de vidas caso vidas_restantes > 0
                if nave.vidas_restantes == 1:
                    engine.say("Uma vida restante")

                # Game_Over
                elif nave.vidas_restantes < 1:
                    nave.vidas_restantes = 5
                    for ast in grupo_asteroides:
                        ast.kill()
                        ast.destroy()
                    game_over()

                else:
                    engine.say(f"{nave.vidas_restantes} vidas restantes")
                engine.runAndWait()
            # se nao aconteceu nada so atualiza
            else:
                asteroide.update()


        # desenha informacoes na tela
        grupo_asteroides.draw(surface)

        # blind_mode exibe apenas a nave em um fundo preto
        if blind_mode:
            surface.fill(values.PRETO)

        # desenha vida
        draw_life()
        grupo_naves.draw(surface)
        # atualiza a nave
        nave.update(surface)
        pygame.display.update()

    pygame.quit()


def blind_game_start():
    """
    Inicia o jogo com Blind Mode ativado
    """
    game_start(True)


def game_over():
    """
    Define o Game Over como menu atual
    """
    engine.say("Fim de jogo")
    engine.runAndWait()
    current_menu = gameover.get_current()
    current_menu.mainloop(surface)

def main_menu():
    """
    Define o Menu principal como menu atual
    """
    current_menu = menu.get_current()
    current_menu.mainloop(surface)


def inicio_jogo():
    """
    Contando a historia no inicio do jogo
    """
    # controlador pra sair
    run = True

    # inicio em audio
    inicio.play()
    while run:
        for event in pygame.event.get():
            # se a pessoa sair encerra o jogo
            if event.type == pygame.QUIT:
                exit()
            # se a pessoa apertar qualquer tecla
            if event.type == pygame.KEYDOWN:
                run = False
        if not pygame.mixer.get_busy():
            run = False
    pygame.mixer.stop()



def instructions():
    """
    Exibe imagem com as intstrucoes do jogo
    """
    # controlador pra sair
    run = True

    # instrucoes em audio
    instrucoes.play()
    while run:

        # desenha fundo
        instructions_bg = pygame.image.load("assets/images/instrucoes.jpg")
        surface.blit(instructions_bg, (0, 0))

        for event in pygame.event.get():
            # se a pessoa sair encerra o jogo
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                # se a pessoa aperta enter inicia o jogo
                if event.key == pygame.K_RETURN:
                    pygame.mixer.stop()
                    game_start()
                # se a pessoa aperta seta esquerda volta pro menu
                if event.key == pygame.K_LEFT:
                    pygame.mixer.stop()
                    menu.mainloop(surface)

        pygame.display.update()

    pygame.quit()


# Mensagem antes de aparecer o menu
# Futuramente contara a historia do jogo
draw_bg()
pygame.display.update()
inicio_jogo()
# engine.say("Bem vindo ao Milkway")
# engine.runAndWait()

# Carrega imagem de fundo do Menu
myimage = pygame_menu.baseimage.BaseImage(
    image_path="assets/images/espaço.gif",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
)

# Define a fonte do texto do Menu
font = pygame_menu.font.FONT_8BIT

# Cria a Theme do Menu
menutheme = pygame_menu.themes.Theme(
    title_background_color=(0, 0, 0),
    background_color=myimage,
    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
    widget_font=font,
    title_font=font,
    title_offset=(300, 100),
)

# Cria a Theme do Game Over
gameovertheme = pygame_menu.themes.Theme(
    title_background_color=(0, 0, 0),
    background_color=(0, 0, 0),
    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
    widget_font=font,
    title_font=font,
    title_offset=(300, 100),
)

# Cria o Menu principal
menu = pygame_menu.Menu(screen_height, screen_width, 'MilkWay', theme=menutheme)
# Adiciona botoes com voz descritiva
btn = menu.add_button('Jogar', game_start)
btn.add_draw_callback(speakButton)
btn = menu.add_button('Instrucoes', instructions)
btn.add_draw_callback(speakButton)
btn = menu.add_button('Blind Mode', blind_game_start)
btn.add_draw_callback(speakButton)
btn = menu.add_button('Sair', pygame_menu.events.EXIT)
btn.add_draw_callback(speakButton)

# Cria o menu de Game Over
gameover = pygame_menu.Menu(screen_height, screen_width, 'GAMEOVER', theme=gameovertheme)
# Adiciona botoes com voz descritiva
btn = gameover.add_button('Voltar', main_menu)
btn.add_draw_callback(speakButton)
btn = gameover.add_button('Sair', pygame_menu.events.EXIT)
btn.add_draw_callback(speakButton)

main_menu()

pygame.quit()
oal.oalQuit()

