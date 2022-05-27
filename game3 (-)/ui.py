import pygame

class UI:
    def __init__(self,surface):

        self.display_surface = surface

        self.flower = pygame.image.load('graphics/ui/flower.png').convert_alpha()
        self.flower_rect = self.flower.get_rect(topleft = (50,61))
        self.font = pygame.font.Font('graphics/ui/ARCADEPI.ttf',30)

    def show_coins(self,amount):
        self.display_surface.blit(self.flower,self.flower_rect)
        flower_amount_surf = self.font.render(str(amount),False,'#33323d')
        flower_amount_rect = flower_amount_surf.get_rect(midleft = (self.flower_rect.right + 4,self.flower_rect.centery))
        self.display_surface.blit(flower_amount_surf,flower_amount_rect)