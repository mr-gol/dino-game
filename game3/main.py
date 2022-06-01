import pygame, sys
from settings import *
from level import Level
from game_data import level_0
from ui import UI
import button

#в данном файле инициируем саму игру

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

#подгружаем окно игры и название окна
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dino")
clock = pygame.time.Clock()
game = Game()
start = False
#font = pygame.font.Font('tutfancybukvy', 50)

bg_surface = pygame.image.load('graphics/bg.png').convert()
start_img = pygame.image.load('graphics/start.png').convert_alpha()
exit_img = pygame.image.load('graphics/exit.png').convert_alpha()

start_button = button.Button(100, 200, start_img, 0.8)
exit_button = button.Button(480, 200, exit_img, 0.8)

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
