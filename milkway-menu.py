import pygame
import values


class Option:
    def __init__(self, text, x, y):
        font_t = pygame.font.SysFont("Comic Sans MS", 15)
        self.text = text
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 150, 25)
        self.text_t = font_t.render(text, False, values.BRANCO)
        self.cor = values.AZUL

    def set_selected(self):
        """Muda a opcao para ser selecionada"""
        self.rect.width = 180
        self.cor = values.VERMELHO

    def print_option(self, win):
        """Printa a opcao"""
        pygame.draw.rect(win, self.cor, self.rect)
        win.blit(self.text_t, (self.x+10, self.y+3))


class Menu:
    def __init__(self, options, win):
        self.options = options
        self.win = win
        self.selected = 0

    def loop(self):
        run = True
        while run:
            e = pygame.event.get()
            self.atualiza_selected(pygame.event.get())
            if e.type == pygame.K_SPACE:
                self.options[self.selected][1]()

    def atualiza_selected(self, e):
        """Recebe os eventos e atualiza a opcao selecionada"""
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                self.selected -= 1
                if self.selected < 0:
                    self.selected = len(self.options) - 1
            if e.key == pygame.K_DOWN:
                self.selected += 1
                if self.selected > len(self.options) - 1:
                    self.selected = 0

    def print_win(self):
        """Printa uma tela com destaque na opcao selecionada"""
        font = pygame.font.SysFont("Comic Sans MS", 30)
        title = font.render("PyBird", False, values.BRANCO)
        desc = font.render("Pressione espaço para iniciar", False, values.BRANCO)
        options = []
        for i in range(len(self.options)):
            option = Option(self.options[i], 10, (i + 1) * 100)
            if i == self.selected:
                option.set_selected()
            options.append(option)
        self.win.fill((0, 0, 0))
        self.win.blit(title, (0, 0))
        self.win.blit(desc, (0, 50))
        for option in options:
            option.print_option(self.win)