import pygame
import pygame_menu

#fts do jogo
clock = pygame.time.Clock()
fps = 60

#iniciar a tela
pygame.init()
screen_width = 600
screen_height = 337
screen = pygame.display.set_mode((screen_width, screen_height), 0)
pygame.display.set_caption('MilkWay')

#carrega imagem
bg = pygame.image.load("viaLactea.jpg")


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
        self.image = pygame.image.load("naveEspacial.png")
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


rum = True
while rum:

    #fps da tela
    clock.tick(fps)

    #desenha fundo
    draw_bg()

    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           rum = False

    nave.movimento()
    grupo_naves.draw(screen)
    pygame.display.update()

pygame.quit()
