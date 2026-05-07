import pygame
from settings import WIDTH, HEIGHT

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.idle_width = 84
        self.idle_height = 84
        self.walk_width = 64
        self.walk_height = 64
        self.width = 48
        self.height = 48
        self.speed = 3

        # --- Carrega frames de animação ---
        self.walk_frames = [
            pygame.transform.scale(
                pygame.image.load(f"baribe-main/assets/sprites/player/cici1_00{i}.png").convert_alpha(),
                (self.walk_width, self.walk_height)
            )
            for i in range(0, 6)  # walk_1 até walk_6
        ]

        self.idle_frames = [
            pygame.transform.scale(
                pygame.image.load(f"baribe-main/assets/sprites/playerempe/cici_em_pé_00{i}.png").convert_alpha(),
                (self.idle_width, self.idle_height)
            )
            for i in range(0, 12)  # idle_1 até idle_14
        ]

        # --- Controle de animação ---
        self.current_frames = self.idle_frames
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 8  # quanto menor, mais rápido

        self.moving = False
        self.facing_right = True  # para espelhar o sprite

    # ----------------------
    # MOVE
    # ----------------------
    def move(self):
        keys = pygame.key.get_pressed()
        self.moving = False

        if keys[pygame.K_a]:
            self.x -= self.speed
            self.moving = True
            self.facing_right = False
        if keys[pygame.K_d]:
            self.x += self.speed
            self.moving = True
            self.facing_right = True
        if keys[pygame.K_s]:
            self.y += self.speed
            self.moving = True
        if keys[pygame.K_w]:
            self.y -= self.speed
            self.moving = True

        self.x = max(0, min(self.x, WIDTH - self.walk_width))
        self.y = max(0, min(self.y, HEIGHT - self.walk_height))

        # --- Troca animação ---
        # DEPOIS
        if self.moving:
            if self.current_frames != self.walk_frames:
                self.current_frames = self.walk_frames
                self.frame_index = 0  # reseta o índice ao trocar animação
        else:
            if self.current_frames != self.idle_frames:
                self.current_frames = self.idle_frames
                self.frame_index = 0  # reseta o índice ao trocar animação

    # ----------------------
    # ANIMATE
    # ----------------------
    def animate(self):
        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.current_frames)

    # ----------------------
    # DRAW
    # ----------------------
    def draw(self, screen):
        self.animate()

        image = self.current_frames[self.frame_index]

        # Espelha o sprite quando vai para a esquerda
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        screen.blit(image, (self.x, self.y))