import pygame
import values


class Option:
    """
    Classe auxiliadora de Menu
    """
    def __init__(self, text, x, y):
        """
        Recebe um texto e as coordenadas do canto superior esquerdo
        """
        font_t = pygame.font.SysFont("Comic Sans MS", 15)
        self.text = text
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 150, 25)
        self.text_t = font_t.render(text, False, values.BRANCO)
        self.cor = values.AZUL  # cor padrao é o azul

    def set_selected(self):
        """Muda a opcao para ser selecionada"""
        self.rect.width = 180
        self.cor = values.VERMELHO  # destacada com vermelho

    def print_option(self, win):
        """Printa a opcao na tela"""
        pygame.draw.rect(win, self.cor, self.rect)
        win.blit(self.text_t, (self.x+10, self.y+3))


class Menu:
    def __init__(self, options, image, win, title="Milkway"):
        """
        Recebe um conjunto de opcoes (texto, acao)
        Uma imagem de fundo, a tela do pygame e opcionalmente um titulo
        """
        self.options = options
        self.win = win
        self.selected = 0   # seleciona a primeira opção por padrão
        self.image = image
        self.title = title

    def loop(self):
        """
        Inicia o menu
        """

        # controlador pra sair
        run = True

        while run:
            # printa a tela
            self.print_win()
            e = pygame.event.get()
            for event in e:
                self.atualiza_selected(event)
                if event.type == pygame.KEYDOWN:
                    # se a pessoa clicou em uma tecla que nao seja setinha, executa acao
                    # da opção selecionada
                    if event.key != pygame.K_DOWN and event.key != pygame.K_UP:
                        self.options[self.selected][1]()
                # se a pessoa sair encerra o jogo
                if event.type == pygame.QUIT:
                    exit()
                    run = False
                    break

    def atualiza_selected(self, e):
        """Recebe os eventos e atualiza a opcao selecionada"""
        if e.type == pygame.KEYDOWN:
            # se a pessoa digitou seta pra cima seleciona opcao acima
            if e.key == pygame.K_UP:
                self.selected -= 1
                # no caso da opcao ja ser a primeira vai para a ultima
                if self.selected < 0:
                    self.selected = len(self.options) - 1
            # se a pessoa digitou seta pra baixo seleciona opcao abaixo
            if e.key == pygame.K_DOWN:
                self.selected += 1
                # no caso da opcao ja ser a ultima vai para a primeira
                if self.selected > len(self.options) - 1:
                    self.selected = 0

    def print_win(self):
        """Printa uma tela com destaque na opcao selecionada"""
        font = pygame.font.SysFont("Comic Sans MS", 30)
        # define um titulo e texto
        title = font.render(self.title, False, values.BRANCO)
        desc = font.render("Pressione qualquer tecla para escolher", False, values.BRANCO)

        # options guarda uma lista de objetos Option com o selecionado ja informado
        options = []
        for i in range(len(self.options)):
            option = Option(self.options[i][0], 10, (i + 1) * 100)
            if i == self.selected:
                option.set_selected()
            options.append(option)

        # atualiza a imagem de fundo e desenha ela
        self.image.update()
        self.image.desenha(self.win)
        # escreve o titulo e texto
        self.win.blit(title, (0, 0))
        self.win.blit(desc, (0, 50))

        # desenha os quadrinhos das opcoes na tela
        for option in options:
            option.print_option(self.win)
        pygame.display.update()
