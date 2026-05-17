# entities/seaweed.py
import pygame
import math
import random
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def asset(path):
    return os.path.join(BASE_DIR, path)

class Seaweed:
    SEGMENT_HEIGHT = 12  # fatias menores = movimento mais fluido

    def __init__(self, x, floor):
        self.base_x = x
        self.floor = floor

        # Escolhe aleatoriamente entre os dois corais
        coral_file = random.choice(["coral_1.png", "coral_2.png"])
        raw = pygame.image.load(asset(f"assets/sprites/objetcs/{coral_file}")).convert_alpha()

        # 2x o tamanho original
        new_w = raw.get_width() * 2
        new_h = raw.get_height() * 2
        self.image = pygame.transform.scale(raw, (new_w, new_h))

        self.frame_w = new_w
        self.frame_h = new_h

        # Posição base (fundo da tela)
        self.base_y = floor - self.frame_h

        # Segmentos
        self.num_segments = max(1, self.frame_h // self.SEGMENT_HEIGHT)
        self.segments   = [0.0] * self.num_segments
        self.velocities = [0.0] * self.num_segments

        # Oscilação ambiente — cada alga tem ritmo próprio
        self.time          = random.uniform(0, math.pi * 2)
        self.sway_speed    = random.uniform(0.008, 0.018)   # mais lento = mais pesado
        self.sway_amplitude = random.uniform(3.0, 6.0)      # balanço natural maior

    # ----------------------
    # COLISÃO COM PLAYER
    # ----------------------
    def _check_player(self, player):
        px = player.x + player.width  // 2
        py = player.y + player.height // 2

        # Velocidade do player (usada para dar impulso proporcional)
        keys = pygame.key.get_pressed()
        vel_x = 0
        if keys[pygame.K_a]: vel_x = -1
        if keys[pygame.K_d]: vel_x =  1

        for i in range(self.num_segments):
            seg_y  = self.base_y + i * self.SEGMENT_HEIGHT
            seg_cx = self.base_x + self.frame_w // 2 + self.segments[i]
            seg_cy = seg_y + self.SEGMENT_HEIGHT // 2

            dx   = px - seg_cx
            dy   = py - seg_cy
            dist = math.hypot(dx, dy)

            touch_radius = player.width * 0.75

            if dist < touch_radius and dist > 0:
                # Força: proporcional à proximidade + direção do player
                force  = (touch_radius - dist) / touch_radius
                push_x = -(dx / dist) * force * 8.0
                push_x += vel_x * force * 4.0   # empurra mais na direção do movimento
                self.velocities[i] += push_x

    # ----------------------
    # UPDATE
    # ----------------------
    def update(self, player):
        self.time += self.sway_speed

        self._check_player(player)

        for i in range(self.num_segments):
            # Influência cresce do fundo pro topo (base quase não se move)
            t = (i / max(1, self.num_segments - 1)) ** 1.5  # curva suave

            # Oscilação natural: segmentos superiores lideram o balanço
            phase   = self.time + i * 0.25
            ambient = math.sin(phase) * self.sway_amplitude * t

            # Segmento herda um pouco do movimento do vizinho de baixo (propagação)
            if i > 0:
                inherit = self.segments[i - 1] * 0.3
            else:
                inherit = 0.0

            target = ambient + inherit

            # Mola em direção ao target
            spring = (target - self.segments[i]) * 0.06
            self.velocities[i] += spring
            self.velocities[i] *= 0.88  # amortecimento suave (mais flutuante)

            self.segments[i] += self.velocities[i]

            # Limite de dobramento
            max_bend = self.frame_w * 0.5
            self.segments[i] = max(-max_bend, min(max_bend, self.segments[i]))

    # ----------------------
    # DRAW
    # ----------------------
    def draw(self, screen):
        seg_h = self.frame_h // self.num_segments

        for i in range(self.num_segments):
            # Garante que a fatia não ultrapasse a altura da imagem
            y_start = i * seg_h
            y_end   = min(y_start + seg_h, self.frame_h)
            actual_h = y_end - y_start

            if actual_h <= 0:
                continue

            slice_rect = pygame.Rect(0, y_start, self.frame_w, actual_h)
            slice_surf = self.image.subsurface(slice_rect)

            draw_x = int(self.base_x + self.segments[i])
            draw_y = self.base_y + y_start

            screen.blit(slice_surf, (draw_x, draw_y))