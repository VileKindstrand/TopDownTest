from turtle import delay
import pygame
from config import *
import math
import random
import time

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (1,0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.animation_loop = 1  
        self.facing = 'right' 



        #spelarens utseende
        self.image = self.game.character_spritesheet.get_sprite(33, 0, 32, 48)
        #hitbox
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):

        self.movement()
        self.animation()

        self.rect.x += self.x_change         # VID DIAGONAL LINJE RÖR MAN SIG SNABBARE; FIXA "NORMALIZED VECTOR". Vet dock inte hur det här fungerar än
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.y_change = 0
        self.x_change = 0



    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change  -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width       #vid kollision mellan block och player kommer spelaren först teleporteras in i blocket och sedan flyttas en tiles längd tillbaka där spelaren kom ifrån, vilket kommer leda till att spelaren hamnar vid blockets vägg
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height    #vid kollision mellan block och player kommer spelaren först teleporteras in i blocket och sedan flyttas en tiles längd tillbaka där spelaren kom ifrån, vilket kommer leda till att spelaren hamnar vid blockets vägg
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def animation(self):
        
        left_animation = [self.game.character_spritesheet.get_sprite(1, 0, self.width, 33),          #degposition
                          self.game.character_spritesheet.get_sprite(34, 0, self.width, 48),         #låg hopp
                          self.game.character_spritesheet.get_sprite(67, 0, self.width, 48)]      #hög hopp

        right_animation = [self.game.character_spritesheet.get_sprite(67, 48, self.width, 48),
                          self.game.character_spritesheet.get_sprite(35, 48, self.width, 48),         
                          self.game.character_spritesheet.get_sprite(2, 48, self.width, 48)]

        up_animation = [self.game.character_spritesheet.get_sprite(1, 0, self.width, 48),         
                          self.game.character_spritesheet.get_sprite(34, 0, self.width, 48),      
                          self.game.character_spritesheet.get_sprite(67, 0, self.width, 48)]      

        down_animation = [self.game.character_spritesheet.get_sprite(67, 48, self.width, 48),          
                          self.game.character_spritesheet.get_sprite(35, 48, self.width, 48),         
                          self.game.character_spritesheet.get_sprite(1, 48, self.width, 48)]

        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 0, self.width, 48)
                self.animation_loop = 1
            else:
                self.image = left_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.05
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(67, 48, self.width, 48)
                self.animation_loop = 1
            else:
                self.image = right_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.05
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 0, self.width, 48)
                self.animation_loop = 1
            else:
                self.image = up_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.05
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(67, 48, self.width, 48)
                self.animation_loop = 1
            else:
                self.image = down_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.05
                if self.animation_loop >= 3:
                    self.animation_loop = 1





class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height =  TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(0, 32, 33, 32)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Kenny(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height =  TILESIZE

        self.image = self.game.villagers_spritesheet.get_sprite(33, 0, 32, 48)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Vile(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height =  TILESIZE

        self.image = self.game.villagers_spritesheet.get_sprite(66, 0, 32, 48)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

class Trunk(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height =  TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(0, 64, 32, 32)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height =  TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(0, 0, 33, 32)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

class Hitbox(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height =  TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y