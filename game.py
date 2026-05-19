import pygame
import random

from settings import WIDTH, HEIGHT, FPS

from entities.player import Player
from entities.fish import Fish
from entities.particle import Particle
from entities.trash import Trash
from entities.seaweed import Seaweed
from entities.oxygen_bubble import OxygenBubble

class Game:
    def __init__(self):

        # --- Initialize pygame ---
        pygame.init()
        pygame.mixer.init()
        self.score = 0

        # --- Window configuration ---
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("BARIBE")

        # --- FPS control ---
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load("assets/sprites/objetcs/cenario_boa_viagem.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # --- Underwater overlay ---
        self.water_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.water_overlay.fill((20, 90, 140, 70))
        
        # --- Game state ---
        self.running = True

        self.floor = HEIGHT

        self.water_time = 0

        # --- Entities ---
        self.player = Player(600, 350)

        # --- Fish entities (aquarium fish) ---
        self.fishes = []

        self.max_fishes = 35
        self.fish_spawn_delay = 300
        self.last_fish_spawn = pygame.time.get_ticks()

        # --- Particle system (bubbles) ---
        self.particles = []
        # --- Player breathing bubbles ---
        self.player_bubble_delay = random.randint(1200, 3000)  # 1.2s até 3s
        self.last_player_bubble = pygame.time.get_ticks()

        # --- Font's ---
        self.font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 10)

        # --- Oxygen bubbles collectible ---
        self.oxygen_bubbles = []

        self.oxygen_spawn_delay = 5000  # nasce uma a cada 5 segundos
        self.last_oxygen_spawn = pygame.time.get_ticks()

        self.oxygen_bubble_img = pygame.image.load(
            "assets/sprites/objetcs/bubble.png"
        ).convert_alpha()

        self.oxygen_bubble_img = pygame.transform.scale(
            self.oxygen_bubble_img,
            (28, 28)
        )

        self.oxygen_sound = pygame.mixer.Sound(
            "assets/sounds/bubble-pop.mp3"
        )


        self.oxygen_bubbles = []

        self.oxygen_spawn_delay = 5000  # 5 segundos
        self.last_oxygen_spawn = pygame.time.get_ticks()


        # --- Background music ---
        pygame.mixer.music.load(
            "assets/sounds/diving.mp3"
        )


        pygame.mixer.music.set_volume(0.4)
        
        pygame.mixer.music.play(-1)

        self.fish_flee_sound = pygame.mixer.Sound(
            "assets/sounds/fish-sound.mp3"
        )

        self.fish_flee_sound.set_volume(0.4)
        self.fish_flee_channel = pygame.mixer.Channel(1)
        
        self.trashes = []

        for i in range(10):
            x = random.randint(50, WIDTH - 50)
            trash = Trash(x, self.floor)
            self.trashes.append(trash)

# --- Trash respawn ---
        self.trash_respawn_delay = 5000  # 5 segundos após limpar tudo
        self.trash_respawn_timer = None  # None = não está contando
        self.trash_amount = 10           # quantos lixos spawnar no respawn

        self.seaweed_img = pygame.image.load("assets/sprites/objetcs/coral_1.png").convert_alpha()
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
                            break

    # ----------------------
    # BUBBLE SPAWN
    # ----------------------
    def spawn_bubble(self, x, y):

        bubble = Particle(x, y)

        self.particles.append(bubble)

    def spawn_oxygen_bubbles(self):
        now = pygame.time.get_ticks()

        if now - self.last_oxygen_spawn >= self.oxygen_spawn_delay:
            x = random.randint(60, WIDTH - 60)
            y = random.randint(80, HEIGHT - 80)

            bubble = OxygenBubble(x, y, self.oxygen_bubble_img)

            self.oxygen_bubbles.append(bubble)

            self.last_oxygen_spawn = now


    def update_oxygen_bubbles(self):
        for bubble in self.oxygen_bubbles:
            bubble.update()

        self.oxygen_bubbles = [
            bubble for bubble in self.oxygen_bubbles
            if not bubble.is_off_screen()
        ]


    def check_oxygen_collision(self):
        player_rect = self.player.get_rect()

        for bubble in self.oxygen_bubbles[:]:
            if player_rect.colliderect(bubble.rect):
                self.oxygen_bubbles.remove(bubble)
                self.player.add_oxygen(20)
                self.oxygen_sound.play()

    def spawn_player_bubbles(self):
        now = pygame.time.get_ticks()

        if now - self.last_player_bubble >= self.player_bubble_delay:

            # posição da bolha perto da cabeça / boca do player
            bubble_x = self.player.x + 35
            bubble_y = self.player.y + 20

            # se estiver virado para esquerda, muda o lado da bolha
            if not self.player.facing_right:
                bubble_x = self.player.x + 15

            # solta várias bolhinhas, como respiração
            for _ in range(random.randint(2, 5)):
                x = bubble_x + random.randint(-4, 4)
                y = bubble_y + random.randint(-4, 4)

                self.particles.append(Particle(x, y))

            # próximo tempo aleatório
            self.player_bubble_delay = random.randint(1200, 3000)
            self.last_player_bubble = now

    # ----------------------
    # TRASH RESPAWN
    # ----------------------
    def check_trash_respawn(self):
        now = pygame.time.get_ticks()

        todos_coletados = all(t.coletado for t in self.trashes)

        if todos_coletados and self.trash_respawn_timer is None:
            self.trash_respawn_timer = now

        if self.trash_respawn_timer and now - self.trash_respawn_timer >= self.trash_respawn_delay:
            self.trashes = []
            for _ in range(self.trash_amount):
                x = random.randint(50, WIDTH - 50)
                self.trashes.append(Trash(x, self.floor))
            self.trash_respawn_timer = None

    # ----------------------
    # UPDATE
    # ----------------------
    def update(self, dt):
        ...

    # ----------------------
    # UPDATE
    # ----------------------
    def update(self, dt):

        self.player.move()
        self.check_trash_respawn()
        self.spawn_oxygen_bubbles()
        self.update_oxygen_bubbles()
        self.check_oxygen_collision()

        self.spawn_player_bubbles()
        self.player.update_oxygen(dt)

        # Spawn gradual dos peixes
        now = pygame.time.get_ticks()

        if len(self.fishes) < self.max_fishes:
            if now - self.last_fish_spawn >= self.fish_spawn_delay:
                fish = Fish(self)
                self.fishes.append(fish)
                self.last_fish_spawn = now

        for fish in self.fishes:
            fish.move(self.fishes)

        # cria bolhas aleatórias
        if random.random() < 0.1:

            x = random.randint(0, WIDTH)
            y = HEIGHT

            particle = Particle(x, y)

            self.particles.append(
                Particle(x, y, from_player=True)
            )

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

        for bubble in self.oxygen_bubbles:
            bubble.draw(self.screen)

        # player
        self.player.draw(self.screen)
        self.player.draw_oxygen_bar(self.screen)

        # Algas
        for seaweed in self.seaweeds:
            seaweed.draw(self.screen)

        #Lixo
        for trash in self.trashes:
            trash.draw(self.screen, self.font, self.player)

        # peixes    

        for fish in self.fishes:
            fish.draw(self.screen)

        self.screen.blit(self.water_overlay, (0, 0))
        texto_score = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(texto_score, (10, 10))  # canto superior esquerdo

        pygame.display.update()

    # ----------------------
    # RUN
    # ----------------------
    def run(self):

        while self.running:

            dt = self.clock.tick(FPS) / 1000

            self.events()
            self.update(dt)
            self.draw()

        pygame.quit()