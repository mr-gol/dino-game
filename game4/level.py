import pygame, sys
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tile import Tile, StaticTile, AnimatedTile, Flower
from player import Player
from human import Human
import button

#в данном файле описываем перемещения героя,
#подгружаем графику героя на все случаи жизни,
#проверяем, где он, как он :) на земле ли
#отслеживаем все положения в self

pygame.mixer.init()
bg_music = pygame.mixer.Sound('audio/bg_music.mp3')
screen = pygame.display.set_mode((screen_width, screen_height))

class Level(pygame.sprite.Sprite):
    #подгружаем графику
    def __init__(self, level_data, surface, change_flowers, flowers):
        super().__init__()
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None
        self.frame_index = 0
        self.animation_speed = 0
        self.flowers = 0

        bg_music.play(loops=-1)
        self.flower_sound = pygame.mixer.Sound('audio/flower.mp3')

        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        
        # user interface
        self.change_flowers = change_flowers

        ground_layout = import_csv_layout(level_data['ground'])
        self.ground_sprites = self.create_tile_group(ground_layout, 'ground')

        flower_layout = import_csv_layout(level_data['flower'])
        self.flower_sprites = self.create_tile_group(flower_layout, 'flower')

        trash_layout = import_csv_layout(level_data['trash'])
        self.trash_sprites = self.create_tile_group(trash_layout, 'trash')

        human_layout = import_csv_layout(level_data['human'])
        self.human_sprites = self.create_tile_group(human_layout, 'human')

        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraint')

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'ground':
                        ground_tile_list = import_cut_graphics('graphics/ground/ground_tile.png')
                        tile_surface = ground_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)

                    elif type == 'flower':
                        sprite = Flower(tile_size, x, y, 'graphics/flower/flower')

                    elif type == 'trash':
                        trash_tile_list = import_cut_graphics('graphics/trash.png')
                        trash_surface = trash_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, trash_surface)

                    elif type == 'human':
                        sprite = Human(tile_size, x, y)

                    elif type == 'constraint':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    '''def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]'''

    def player_setup(self, layout):
        #спавним игрока, отображаем его
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == '0':
                    sprite = Player((x, y), self.display_surface)
                    self.player.add(sprite)
                elif val == '1':
                    fin_surface = pygame.image.load('graphics/character/fin.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, fin_surface)
                    self.goal.add(sprite)

        if self.kill:
            #что будет, если игрок умрёт
            for row_index, row in enumerate(layout):
                for col_index, val in enumerate(row):
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if val == '0':
                        sprite = Player((x, y), self.display_surface)
                        self.player.add(sprite)
                    elif val == '1':
                        fin_surface = pygame.image.load('graphics/character/fin.png').convert_alpha()
                        sprite = StaticTile(tile_size, x, y, fin_surface)
                        self.goal.add(sprite)

    def human_collision_reverse(self):
        for human in self.human_sprites.sprites():
            if pygame.sprite.spritecollide(human, self.constraint_sprites, False):
                human.reverse()

    def horizontal_movement_collision(self):
        #описываем графику при горизантальном движении,
        #проверяем, куда повёрнут герой
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.ground_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_movement_collision(self):
        #вертикальные движения, как работают прыжки
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.ground_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def scroll_x(self):
        #как герой вращается и как меняется графика
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def get_player_on_ground(self):
        #на земле ли герой?
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    #изменение счета цветочков
    def check_flower_collisions(self):
        collided_flowers = pygame.sprite.spritecollide(self.player.sprite, self.flower_sprites, True)
        if collided_flowers:
            self.flower_sound.play()
            for flower in collided_flowers:
                self.change_flowers(1)
                self.flowers += 1
                
    def check_human_collisions(self):
        human_collision = pygame.sprite.spritecollide(self.player.sprite, self.human_sprites, False)
        if human_collision:
            if self.flowers < 25:
                end1_surface = pygame.image.load('graphics/end1.png').convert()
                screen.blit(end1_surface, (0, 0))
                end1 = pygame.image.load('graphics/end1.png').convert()
                end1_btn = button.Button(0, 0, end1, 1.0)
                if end1_btn.draw(screen):
                    pygame.quit()
                    sys.exit()
            else:
                end2_surface = pygame.image.load('graphics/end2.png').convert()
                screen.blit(end2_surface, (0, 0))
                end2 = pygame.image.load('graphics/end2.png').convert()
                end2_btn = button.Button(0, 0, end2, 1.0   )
                if end2_btn.draw(screen):
                    pygame.quit()
                    sys.exit()

    def run(self):
        #отслеживаем состояние героя по параметрам выше
        self.ground_sprites.update(self.world_shift)
        self.ground_sprites.draw(self.display_surface)

        self.flower_sprites.update(self.world_shift)
        self.flower_sprites.draw(self.display_surface)

        self.trash_sprites.update(self.world_shift)
        self.trash_sprites.draw(self.display_surface)

        self.human_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.human_collision_reverse()
        self.human_sprites.draw(self.display_surface)

        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        
        self.check_flower_collisions()
        self.check_human_collisions()
