import pygame
import random
import math
from settings import WIDTH, HEIGHT
from .particle import Particle


class Fish:

    FISH_TYPES = {
        "piracanjuba": 5,
        "flamengo": 4
    }

    # ----------------------
    # INIT
    # ----------------------
    def __init__(self, game):
        self.game = game

        self.scale = random.uniform(0.5, 1.0)
        self.size = int(52 * self.scale)

        self.particles = []
        self.trail = []
        self.speed_lines = []

        self.time = random.uniform(0, 10)

        self.frame_index = 0
        self.animation_speed = 0.06

        self.run_time = 0
        self.alert_timer = 0

        self.normal_speed = random.uniform(0.5, 1.2) * self.scale
        self.speed = self.normal_speed

        self.respawn()

    # ----------------------
    # SETUP
    # ----------------------
    def _load_frames(self):
        frame_count = self.FISH_TYPES[self.fish_type]
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f"baribe-main/assets/sprites/fishes/{self.fish_type}{i}.png").convert_alpha(),
                (self.size, self.size)
            )
            for i in range(1, frame_count + 1)
        ]

    def respawn(self):
        self.y = random.randint(50, HEIGHT - 50)
        self.direction = random.choice([-1, 1])

        if self.direction == 1:
            self.x = random.randint(-100, -40)
        else:
            self.x = random.randint(WIDTH + 40, WIDTH + 100)

        self.normal_speed = random.uniform(0.5, 1.2)
        self.speed = self.normal_speed

        self.fish_type = random.choice(list(self.FISH_TYPES.keys()))
        self._load_frames()

    # ----------------------
    # MOVE — partes internas
    # ----------------------
    def _update_timers(self):
        if self.run_time > 0:
            self.run_time -= 1
        else:
            self.speed = self.normal_speed
            self.animation_speed = 0.06

        if self.alert_timer > 0:
            self.alert_timer -= 1

    def _move_horizontal(self):
        self.x += self.speed * self.direction

    def _move_vertical(self):
        self.time += 0.05
        self.y += math.sin(self.time) * 0.3

    def _check_player(self):
        player = self.game.player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)

        if distance < 50:
            self._flee(dx, speed=10, anim=0.15)

        elif distance < 90:
            self._flee(dx, speed=6, anim=0.12)

        else:
            self.animation_speed = 0.06

    def _flee(self, dx, speed, anim):
        self.direction = -1 if dx > 0 else 1

        if self.run_time == 0:
            self.alert_timer = 40

        self.speed = speed
        self.animation_speed = anim
        self.run_time = 30

    def _check_bounds(self):
        if self.x > WIDTH + 120 or self.x < -120:
            self.respawn()

    def _update_animation(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

    def _update_particles(self):
        if self.speed > 3:
            px = self.x if self.direction == 1 else self.x + 64
            if random.random() < 0.7:
                self.particles.append(
                    Particle(
                        px + random.uniform(-3, 3),
                        self.y + 32 + random.uniform(-3, 3)
                    )
                )

        for particle in self.particles:
            particle.update()

        self.particles = [p for p in self.particles if p.life > 0 and p.size > 0.5]

    def _update_speed_lines(self):
        if self.speed > 3:
            lx = self.x if self.direction == 1 else self.x + self.size
            if random.random() < 0.5:
                self.speed_lines.append({
                    "x": lx,
                    "y": self.y + random.randint(0, max(1, self.size - 1)),
                    "length": random.randint(15, 35),
                    "life": 8
                })

        for line in self.speed_lines:
            line["x"] -= self.direction * 0.5
            line["life"] -= 1

        self.speed_lines = [l for l in self.speed_lines if l["life"] > 0]

    # ----------------------
    # MOVE — público
    # ----------------------
    def move(self, fishes):
        self._update_timers()
        self._move_horizontal()
        self._move_vertical()
        self._update_speed_lines()
        self._update_particles()
        self._check_player()
        self._check_bounds()
        self._update_animation()

    # ----------------------
    # DRAW — partes internas
    # ----------------------
    def _draw_speed_lines(self, screen):
        for line in self.speed_lines:
            alpha = int((line["life"] / 8) * 180)
            surface = pygame.Surface((line["length"], 2), pygame.SRCALPHA)
            surface.fill((255, 255, 255, alpha))
            screen.blit(surface, (line["x"] - line["length"] // 2, line["y"]))

    def _draw_particles(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def _draw_sprite(self, screen):
        sprite = self.frames[int(self.frame_index)]

        if self.direction == -1:
            sprite = pygame.transform.flip(sprite, True, False)

        if self.run_time > 0:
            t = self.run_time / 30
            new_w = int(self.size * (1.0 - 0.35 * t))
            new_h = int(self.size * (1.0 - 0.5 * t))
            sprite = pygame.transform.scale(sprite, (new_w, new_h))
            offset_x = (self.size - new_w) // 2
            offset_y = (self.size - new_h) // 2
            screen.blit(sprite, (self.x + offset_x, self.y + offset_y))
        else:
            screen.blit(sprite, (self.x, self.y))

    def _draw_alert(self, screen):
        if self.alert_timer > 0:
            font = pygame.font.SysFont("Arial", 30, bold=True)
            alpha = min(255, self.alert_timer * 10)
            exclamation = font.render("!", True, (255, 220, 0))
            exclamation.set_alpha(alpha)
            screen.blit(exclamation, (self.x + self.size // 2 - 5, self.y - 24))

    # ----------------------
    # DRAW — público
    # ----------------------
    def draw(self, screen):
        self._draw_speed_lines(screen)
        self._draw_particles(screen)
        self._draw_sprite(screen)
        self._draw_alert(screen)