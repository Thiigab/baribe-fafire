import pygame
import random
import math
from settings import WIDTH, HEIGHT

class Bubble:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH)
        self.y = HEIGHT + random.randint(0, 100)
        self.size = random.randint(3, 10)
        self.speed = random.uniform(0.5, 2.0)
        self.wobble = random.uniform(0, math.pi * 2)
        self.wobble_speed = random.uniform(0.02, 0.05)
        self.alpha = random.randint(80, 180)

    def update(self):
        self.y -= self.speed
        self.wobble += self.wobble_speed
        self.x += math.sin(self.wobble) * 0.5

        if self.y < -20:
            self.reset()

    def draw(self, screen):
        surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (200, 230, 255, self.alpha), (self.size, self.size), self.size)
        pygame.draw.circle(surface, (255, 255, 255, 60), (self.size - 2, self.size - 2), self.size // 3)
        screen.blit(surface, (int(self.x - self.size), int(self.y - self.size)))


class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.text = text
        self.font = font
        self.hovered = False

        self.color_normal = (10, 60, 120, 180)
        self.color_hover  = (20, 120, 200, 220)
        self.color_border = (80, 180, 220)
        self.color_border_hover = (150, 230, 255)

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed

    def draw(self, screen):
        color = self.color_hover if self.hovered else self.color_normal
        border_color = self.color_border_hover if self.hovered else self.color_border

        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        surface.fill(color)
        screen.blit(surface, self.rect.topleft)

        pygame.draw.rect(screen, border_color, self.rect, 2)

        scale = 1.05 if self.hovered else 1.0
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        if self.hovered:
            new_w = int(text_surf.get_width() * scale)
            new_h = int(text_surf.get_height() * scale)
            text_surf = pygame.transform.scale(text_surf, (new_w, new_h))

        tx = self.rect.centerx - text_surf.get_width() // 2
        ty = self.rect.centery - text_surf.get_height() // 2
        screen.blit(text_surf, (tx, ty))


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.action = None  # "play", "quit"

        self.clock = pygame.time.Clock()
        self.time = 0

        # --- Fontes ---
        self.font_title  = pygame.font.Font("assets/fonts/PressStart2P.ttf", 32)
        self.font_button = pygame.font.Font("assets/fonts/PressStart2P.ttf", 12)
        self.font_small  = pygame.font.Font("assets/fonts/PressStart2P.ttf", 7)

        # --- Bolhas decorativas ---
        self.bubbles = [Bubble() for _ in range(40)]

        # --- Botões ---
        cx = WIDTH // 2
        self.btn_play    = Button(cx, HEIGHT // 2 - 10,  260, 45, "JOGAR",    self.font_button)
        self.btn_credits = Button(cx, HEIGHT // 2 + 55, 260, 45, "CRÉDITOS", self.font_button)
        self.btn_quit    = Button(cx, HEIGHT // 2 + 120, 260, 45, "SAIR",     self.font_button)

        # --- Créditos ---
        self.showing_credits = False
        self.credits_lines = [
            "BARIBE",
            "",
            "Desenvolvido por:",
            "Carlos Fernando neto"
            "Thiago Gabriel Santos de Souza",
            "",
            "Arte:",
            "Bia",
            "",
            "Organização do Projeto:",
            "Arthur Rubin, Iago Felipe, Emilayne",
            "Pressione ESC para voltar",
        ]

        # --- Overlay de água ---
        self.water_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.water_overlay.fill((10, 60, 120, 120))

    # ----------------------
    # ONDAS DO FUNDO
    # ----------------------
    def draw_background(self):
        # Gradiente de fundo
        for i in range(HEIGHT):
            t = i / HEIGHT
            r = int(5  + t * 10)
            g = int(20 + t * 60)
            b = int(80 + t * 80)
            pygame.draw.line(self.screen, (r, g, b), (0, i), (WIDTH, i))

        # Ondas animadas
        for wave in range(3):
            offset = wave * 80
            alpha  = 30 - wave * 8
            amp    = 12 - wave * 3
            speed  = 0.015 + wave * 0.005

            points = [(0, HEIGHT)]
            for x in range(0, WIDTH + 10, 6):
                y = int(120 + offset + math.sin(x * 0.008 + self.time * speed * 60) * amp)
                points.append((x, y))
            points.append((WIDTH, HEIGHT))

            if len(points) > 2:
                surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                pygame.draw.polygon(surf, (40, 130, 200, alpha), points)
                self.screen.blit(surf, (0, 0))

    # ----------------------
    # TELA DE CRÉDITOS
    # ----------------------
    def draw_credits(self):
        # Fundo semitransparente
        overlay = pygame.Surface((700, 460), pygame.SRCALPHA)
        overlay.fill((5, 30, 80, 210))
        self.screen.blit(overlay, (WIDTH // 2 - 350, HEIGHT // 2 - 230))
        pygame.draw.rect(self.screen, (80, 180, 220),
                         (WIDTH // 2 - 350, HEIGHT // 2 - 230, 700, 460), 2)

        for i, line in enumerate(self.credits_lines):
            if i == 0:
                surf = self.font_button.render(line, True, (150, 230, 255))
            else:
                surf = self.font_small.render(line, True, (200, 230, 255))

            x = WIDTH // 2 - surf.get_width() // 2
            y = HEIGHT // 2 - 190 + i * 38
            self.screen.blit(surf, (x, y))

    # ----------------------
    # RUN
    # ----------------------
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.time += dt

            mouse_pos     = pygame.mouse.get_pos()
            mouse_clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.action = "quit"
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.showing_credits:
                        self.showing_credits = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked = True

            # --- Update ---
            for bubble in self.bubbles:
                bubble.update()

            if not self.showing_credits:
                self.btn_play.update(mouse_pos)
                self.btn_credits.update(mouse_pos)
                self.btn_quit.update(mouse_pos)

                if self.btn_play.is_clicked(mouse_pos, mouse_clicked):
                    self.action = "play"
                    self.running = False

                if self.btn_credits.is_clicked(mouse_pos, mouse_clicked):
                    self.showing_credits = True

                if self.btn_quit.is_clicked(mouse_pos, mouse_clicked):
                    self.action = "quit"
                    self.running = False

            # --- Draw ---
            self.draw_background()

            for bubble in self.bubbles:
                bubble.draw(self.screen)

            self.screen.blit(self.water_overlay, (0, 0))

            if self.showing_credits:
                self.draw_credits()
            else:
                # Título com sombra
                title_shadow = self.font_title.render("BARIBE", True, (0, 20, 60))
                title_text   = self.font_title.render("BARIBE", True, (150, 230, 255))
                tx = WIDTH // 2 - title_text.get_width() // 2
                ty = HEIGHT // 2 - 140
                self.screen.blit(title_shadow, (tx + 3, ty + 3))
                self.screen.blit(title_text,   (tx, ty))

                # Subtítulo
                sub = self.font_small.render("Limpe o oceano!", True, (180, 220, 255))
                self.screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, ty + 55))

                # Botões
                self.btn_play.draw(self.screen)
                self.btn_credits.draw(self.screen)
                self.btn_quit.draw(self.screen)

            pygame.display.update()

        return self.action