import pygame
import sys
from settings import *
from level import Level
from game_data import level_0
import button
from ui import UI

pygame.font.init()

class Game:
	def __init__(self):
        
		# game attributes
		self.flowers = 0

		# user interface
		self.ui = UI(screen)

		self.level = Level(level_0, screen,self.change_flowers)

	def change_flowers(self,amount):
		self.flowers += amount

	def run(self):
		self.level.run()
		self.ui.show_flowers(self.flowers)
        

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dino")
clock = pygame.time.Clock()
start = False
bg_surface = pygame.image.load('graphics/bg.png').convert()


start_img = pygame.image.load('graphics/start.png').convert_alpha()
exit_img = pygame.image.load('graphics/exit.png').convert_alpha()

start_button = button.Button(100, 200, start_img, 0.8)
exit_button = button.Button(480, 200, exit_img, 0.8)


game = Game()

while True:
    screen.blit(bg_surface, (0, 0))

    if start:
        screen.blit(bg_surface, (0, 0))
        game.run()

    if start_button.draw(screen):
        start = True
    if exit_button.draw(screen):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    pygame.display.update()
    clock.tick(60)
