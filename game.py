import pygame
import random

from settings import WIDTH, HEIGHT, FPS

from entities.player import Player
from entities.fish import Fish
from entities.particle import Particle
from entities.trash import Trash
from entities.seaweed import Seaweed

class Game:
    def __init__(self):

        # --- Initialize pygame ---
        pygame.init()
        self.score = 0

        # --- Window configuration ---
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("BARÉ")

        # --- FPS control ---
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load("baribe-main/assets/sprites/objetcs/cenario_boa_viagem.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        
        # --- Game state ---
        self.running = True

        self.floor = HEIGHT

        # --- Entities ---
        self.player = Player(600, 350)

        # --- Fish entities (aquarium fish) ---
        self.fishes = []
        for i in range(10):
            fish = Fish(self)
            self.fishes.append(fish)

        # --- Particle system (bubbles) ---
        self.particles = []

        # --- Font's ---
        self.font = pygame.font.Font("baribe-main/assets/fonts/PressStart2P.ttf", 10)

        
        self.trashes = []

        for i in range(10):

            x = random.randint(50, WIDTH - 50)

            trash = Trash(x, self.floor)

            self.trashes.append(trash)

        self.seaweed_img = pygame.image.load("baribe-main/assets/sprites/objetcs/coral_1.png").convert_alpha()
        # No __init__, substitui o bloco das seaweeds:
        self.seaweeds = []
        for _ in range(12):
            x = random.randint(30, WIDTH - 30)
            self.seaweeds.append(Seaweed(x, self.floor))

    # ----------------------
    # EVENTS
    # ----------------------
    def events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    for trash in self.trashes:
                        if trash.try_collect(self.player):
                            self.score += 1

    # ----------------------
    # BUBBLE SPAWN
    # ----------------------
    def spawn_bubble(self, x, y):

        bubble = Particle(x, y)

        self.particles.append(bubble)

    # ----------------------
    # UPDATE
    # ----------------------
    def update(self):

        self.player.move()

        for fish in self.fishes:
            fish.move(self.fishes)

        # cria bolhas aleatórias
        if random.random() < 0.1:

            x = random.randint(0, WIDTH)
            y = HEIGHT

            particle = Particle(x, y)

            self.particles.append(particle)

        for particle in self.particles:
            particle.update()

        # remover partículas mortas
        self.particles = [p for p in self.particles if p.life > 0]

        for trash in self.trashes:
            trash.update()

        for seaweed in self.seaweeds:
            seaweed.update(self.player)
    # ----------------------
    # DRAW
    # ----------------------
    def draw(self):

        self.screen.blit(self.background, (0, 0))

        # partículas de fundo (bolhas)
        for particle in self.particles:
            particle.draw(self.screen)

        for seaweed in self.seaweeds:
            seaweed.draw(self.screen)

        self.player.draw(self.screen)

        # peixes
        for fish in self.fishes:
            fish.draw(self.screen)

        # player

        for trash in self.trashes:
            trash.draw(self.screen, self.font, self.player)

        texto_score = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(texto_score, (10, 10))  # canto superior esquerdo

        pygame.display.update()

    # ----------------------
    # RUN
    # ----------------------
    def run(self):

        while self.running:

            self.clock.tick(FPS)

            self.events()
            self.update()
            self.draw()

        pygame.quit()