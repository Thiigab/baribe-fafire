import pygame
import random

class Trash:
    def __init__(self, x, floor):
        # -- Size --
        self.width = 64
        self.height = 64

        # --- Position ---
        self.x = x
        self.y = floor - self.height

        self.coletado = False

        # --- Physics ---
        self.vel_y = 0
        self.vel_x = 0
        self.gravity = 0.03
        self.on_floor = False
        self.floor = floor
        self.friction = 0.9

        # --- Rotation ---
        self.angle = 0
        self.vel_rotation = 0

        # --- Image ---
        self.image = pygame.transform.scale(
            pygame.image.load("assets/sprites/objetcs/bottle.png").convert_alpha(),
            (self.width, self.height)
        )
        
    # ----------------------
    # COLLECT
    # ----------------------
    def try_collect(self, player):

        if self.coletado:
            return False 

        dx = player.x - self.x
        dy = player.y - self.y

        if abs(dx) < 80 and abs(dy) < 80:
            self.coletado = True
            return True

        return False
    
    # ----------------------
    # UPDATE
    # ----------------------
    def update(self):

        if not self.on_floor:

            self.vel_y += self.gravity
            self.y += self.vel_y

            self.vel_x *= self.friction
            self.x += self.vel_x

            self.vel_rotation = self.vel_x * 2
            self.angle += self.vel_rotation

            if self.y + self.height >= self.floor:

                self.y = self.floor - self.height
                self.vel_y *= -0.4

                if abs(self.vel_y) < 0.2:
                    self.vel_y = 0
                    self.on_floor = True

    # ----------------------
    # DRAW
    # ----------------------
    def draw(self, screen, font, player):

        if self.coletado:
            return

        imagem_rotacionada = pygame.transform.rotate(self.image, -self.angle)

        rect = imagem_rotacionada.get_rect(
            center=(self.x + self.width // 2, self.y + self.height // 2)
        )

        screen.blit(imagem_rotacionada, rect.topleft)

        dx = player.x - self.x
        dy = player.y - self.y

        perto = abs(dx) < 80 and abs(dy) < 80

        if perto:

            texto = font.render("[E] coletar", True, (200, 235, 255))

            tw = texto.get_width()
            th = texto.get_height()

            padding = 6

            bx = self.x + self.width // 2 - tw // 2 - padding
            by = self.y - th - padding * 2 - 8

            superficie = pygame.Surface(
                (tw + padding * 2, th + padding * 2),
                pygame.SRCALPHA
            )

            superficie.fill((10, 30, 60, 160))

            screen.blit(superficie, (bx, by))

            pygame.draw.rect(
                screen,
                (80, 180, 200),
                (bx, by, tw + padding * 2, th + padding * 2),
                1
            )

            screen.blit(texto, (bx + padding, by + padding))