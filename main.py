import pygame
from menu import Menu
from game import Game

pygame.init()
screen = pygame.display.set_mode((1366, 768))

menu = Menu(screen)
action = menu.run()

if action == "play":
    jogo = Game()
    jogo.run()

pygame.quit()