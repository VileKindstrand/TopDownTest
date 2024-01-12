from turtle import down
import pygame
from config import *
import math
import random

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

        self.facing = 'down'


        #utseende
        image_to_load = pygame.image.load("img/vatten_gecko.png")
        self.image = pygame.Surface([self.width, self.height])
        self.image.blit(image_to_load, (1,0))
        #hitbox
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        

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
                    self.rect.y = hits[0].rect.top - self.rect.height       #vid kollision mellan block och player kommer spelaren först teleporteras in i blocket och sedan flyttas en tiles längd tillbaka där spelaren kom ifrån, vilket kommer leda till att spelaren hamnar vid blockets vägg
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

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

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 
