#Se não rodar ai baixa: pip install pygame-menu
import pygame
import pygame_menu

#fts do jogo
clock = pygame.time.Clock()
fps = 60

#iniciar a tela
pygame.init()
screen_width = 900
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height), 0)
pygame.display.set_caption('MilkWay')

#carrega imagem
bg = pygame.image.load("assets/images/espaço.gif")

#definindo cores
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

#coloca imagem na tela
def draw_bg():
    screen.blit(bg, (0, 0))

#Classe Nave principal
class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y, vida):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/naveEspacial.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vidas_inicio = vida
        self.vidas_restantes = vida

    def movimento(self):
        #pegar movimentos do teclado
        velocidade = 8
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= velocidade
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += velocidade

        #bullet = Asteroides(self.rect.center, self.rect.top)
        #bullet_grup.add(bullet)

        #pintar vidas
        #coração
        pygame.draw.circle(screen, VERMELHO, (20, 20), 5, 0)
        pygame.draw.circle(screen, VERMELHO, (30, 20), 5, 0)
        pygame.draw.polygon(screen, VERMELHO, ((14, 20), (25, 32), (35, 20)), 0)

class Asteroides(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("asteroide.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5

grupo_naves = pygame.sprite.Group()

nave = Nave(int(screen_width/2), screen_height - 50, 3)
grupo_naves.add(nave)

def Game_Start():
    rum = True
    while rum:
        #fps da tela
        clock.tick(fps)

        #desenha fundo
        draw_bg()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                rum = False
                sys.exit()
                
        nave.movimento()
        grupo_naves.draw(screen)
        pygame.display.update()

        pygame.quit()
        break

myimage = pygame_menu.baseimage.BaseImage(
    image_path="assets/images/espaço.gif",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
)

font = pygame_menu.font.FONT_8BIT

mytheme = pygame_menu.themes.Theme(
    title_background_color = (0, 0, 0),
    background_color = myimage,
    title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE,
    widget_font = font,
    title_font = font,
    title_offset = (300,100),
)

menu = pygame_menu.Menu(500, 900, 'MilkWay', theme=mytheme)

menu.add_button('Jogar', Game_Start)
menu.add_button('Instrucoes', pygame_menu.events.EXIT)
menu.add_button('Blind Mode', pygame_menu.events.EXIT)
menu.add_button('Sair', pygame_menu.events.EXIT)

menu.mainloop(screen)