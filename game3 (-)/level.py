import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tile import Tile, StaticTile, AnimatedTile, Flower, Trash
from player import Player
from game_data import levels

pygame.mixer.init()
bg_music = pygame.mixer.Sound('audio/bg_music.mp3')

class Level:
    def __init__(self, level_data, level_0, surface, change_flower):
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None
        bg_music.play(loops=-1)
        self.current_level = level_0

        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        self.change_flower = change_flower

        ground_layout = import_csv_layout(level_data['ground'])
        self.ground_sprites = self.create_tile_group(ground_layout, 'ground')

        flower_layout = import_csv_layout(level_data['flower'])
        self.flower_sprites = self.create_tile_group(flower_layout, 'flower')

        trash_layout = import_csv_layout(level_data['trash'])
        self.trash_sprites = self.create_tile_group(trash_layout, 'trash')

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

                    elif type == 'flower':
                        sprite = Flower(tile_size, x, y, 'graphics/flower/flower')

                    elif type == 'trash':
                        trash_tile_list = import_cut_graphics('graphics/trash.png')
                        trash_surface = trash_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, trash_surface)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
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

    def horizontal_movement_collision(self):
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
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def check_flower_collisions(self):
        collided_flower = pygame.sprite.spritecollide(self.player.sprite, self.flower_sprites, True)
        if collided_flower:
            for flower in collided_flower:
                self.change_flower(1)

    def run(self):
        self.ground_sprites.update(self.world_shift)
        self.ground_sprites.draw(self.display_surface)

        self.flower_sprites.update(self.world_shift)
        self.flower_sprites.draw(self.display_surface)

        self.trash_sprites.update(self.world_shift)
        self.trash_sprites.draw(self.display_surface)

        self.check_flower_collisions()

        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
