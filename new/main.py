import pygame, sys
from settings import *
from level import Level
from game_data import level_0
from ui import UI
import button
from player import Player

#в данном файле инициируем саму игру

pygame.font.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dino")
clock = pygame.time.Clock()
start = False

bg_surface = pygame.image.load('graphics/bg.png').convert()
start_img = pygame.image.load('graphics/start.png').convert_alpha()
exit_img = pygame.image.load('graphics/exit.png').convert_alpha()

start_button = button.Button(100, 200, start_img, 0.8)
exit_button = button.Button(480, 200, exit_img, 0.8)


class Game:
    def __init__(self):
        self.flowers = 0
        self.ui = UI(screen)
        self.level = Level(level_0, screen, self.change_flowers, self.ui.show_flowers())

    def change_flowers(self, amount):
        self.flowers += amount

    def run(self):
        self.level.run()
        self.ui.show_flowers(self.flowers)

game = Game()

while True:
    screen.blit(bg_surface, (0, 0))

    if start_button.draw(screen):
        start = True
    if exit_button.draw(screen):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if start:
        screen.blit(bg_surface, (0, 0))
        game.run()

    pygame.display.update()
    clock.tick(60)