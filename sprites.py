from turtle import delay, distance
import pygame
from config import *
import math

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))       #JÄVLIGASTE FELET JAG VARIT MED OM: HADE RÅKAT SKRIVA (1,0) VILKET FÖRFLYTTADE ALLA SPRITES MED EN X PIXEL
        sprite.set_colorkey(BLACK)
        return sprite

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('arial.ttf', fontsize)
        self.contet = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y


        self.tect = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text.rect)

class Text_box:
    def __init__(self, game, x, y):

        self.game = game
        self.x = x * TILESIZE * 4
        self.y = y * TILESIZE * 2
        self.width = SPRITESHEET_WIDTH
        self.height =  SPRITESHEET_HEIGTH

        self._layer = TEXT_BOX_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.surface(self.x, self.y)
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

class Player(pygame.sprite.Sprite, Text_box):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE*1.5

        self.x_change = 0
        self.y_change = 0

        self.animation_loop = 1  
        self.facing = 'right'    

        #spelarens utseende
        self.image = self.game.character_spritesheet.get_sprite(33, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x -100
        self.rect.y = self.y - 300

        


    def update(self):

        self.movement()
        self.animation()
        self.interact_villagers()

        self.rect.x += self.x_change         # VID DIAGONAL LINJE RÖR MAN SIG SNABBARE; FIXA "NORMALIZED VECTOR". Vet dock inte hur det här fungerar än
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        global y_change
        global x_change
        self.y_change = 0
        self.x_change = 0
        global player_x_pos
        global player_y_pos
        player_x_pos = self.rect.x
        player_y_pos = self.rect.y

        #self.facing = 'left'



    def movement(self):

        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED / (2 ** 0.5)
                sprite.rect.y += PLAYER_SPEED / (2 ** 0.5)
            self.y_change -= PLAYER_SPEED / (2 ** 0.5)
            self.x_change  -= PLAYER_SPEED / (2 ** 0.5)
            self.facing = 'left'
        elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED / (2 ** 0.5)
                sprite.rect.y += PLAYER_SPEED / (2 ** 0.5)
            self.y_change -= PLAYER_SPEED / (2 ** 0.5)
            self.x_change  += PLAYER_SPEED / (2 ** 0.5)
            self.facing = 'right'
        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED / (2 ** 0.5)
                sprite.rect.y -= PLAYER_SPEED / (2 ** 0.5)
            self.y_change += PLAYER_SPEED / (2 ** 0.5)
            self.x_change  -= PLAYER_SPEED / (2 ** 0.5)
            self.facing = 'left'
        elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED / (2 ** 0.5)
                sprite.rect.y -= PLAYER_SPEED / (2 ** 0.5)
            self.y_change += PLAYER_SPEED / (2 ** 0.5)
            self.x_change += PLAYER_SPEED / (2 ** 0.5)
            self.facing = 'right'
        elif keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change  -= PLAYER_SPEED
            self.facing = 'left'
        elif keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        elif keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
        elif keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
        global y_change
        global x_change
        y_change = self.y_change
        x_change = self.x_change
            #self.facing = 'down'
        print(self.rect.y)



    def interact_villagers(self):
        #screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
        self.dialogue_box = False



        hits = pygame.sprite.spritecollide(self, self.game.villagers, False)
        keys = pygame.key.get_pressed()
        self.display_surface = pygame.display.get_surface()
        foreground = pygame.Surface((100, 100))
        if hits:
            print ("hits")
            if keys[pygame.K_LCTRL]:
                self.dialogue_box = not self.dialogue_box
                if self.dialogue_box:
                    print("cool")
                else:
                    print("idk")



    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width       #vid kollision mellan block och player kommer spelaren först teleporteras in i blocket och sedan flyttas en tiles längd tillbaka där spelaren kom ifrån, vilket kommer leda till att spelaren hamnar vid blockets vägg
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += x_change
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += x_change
                
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height    #vid kollision mellan block och player kommer spelaren först teleporteras in i blocket och sedan flyttas en tiles längd tillbaka där spelaren kom ifrån, vilket kommer leda till att spelaren hamnar vid blockets vägg
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += y_change
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += y_change

    def animation(self):
        
        left_animation = [self.game.character_spritesheet.get_sprite(1, 0, self.width, 48),          #degposition
                          self.game.character_spritesheet.get_sprite(33, 0, self.width, 48),         #låg hopp
                          self.game.character_spritesheet.get_sprite(66, 0, self.width, 48)]      #hög hopp

        right_animation = [self.game.character_spritesheet.get_sprite(1, 0, self.width, 48),
                          self.game.character_spritesheet.get_sprite(33, 0, self.width, 48),         
                          self.game.character_spritesheet.get_sprite(66, 0, self.width, 48)]

        up_animation = [self.game.character_spritesheet.get_sprite(1, 0, self.width, 48),         
                          self.game.character_spritesheet.get_sprite(33, 0, self.width, 48),      
                          self.game.character_spritesheet.get_sprite(66, 0, self.width, 48)]      

        down_animation = [self.game.character_spritesheet.get_sprite(1, 0, self.width, 48),          
                          self.game.character_spritesheet.get_sprite(33, 0, self.width, 48),         
                          self.game.character_spritesheet.get_sprite(66, 0, self.width, 48)]

        if self.facing == "left":
            self.old_facing = self.facing
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 0, self.width, 48)
            else:
                self.image = left_animation[math.floor(self.animation_loop)]
                self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                self.animation_loop += 0.05
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 0, self.width, 48)
            else:
                self.image = left_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.05
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "up":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 0, self.width, 48)
            else:
                self.image = left_animation[math.floor(self.animation_loop)]
                self.animation_loop += 0.05
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "down":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 0, self.width, 48)
            else:
                self.image = left_animation[math.floor(self.animation_loop)]
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
        self.width = SPRITESHEET_WIDTH
        self.height =  SPRITESHEET_WIDTH

        self.image = self.game.terrain_spritesheet.get_sprite(0, 32, 33, 32)
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

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
        self.width = SPRITESHEET_WIDTH
        self.height =  SPRITESHEET_WIDTH

        self.image = self.game.terrain_spritesheet.get_sprite(0, 64, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

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
        self.width = SPRITESHEET_WIDTH
        self.height =  SPRITESHEET_WIDTH

        if WATER_LEVEL > 50:
            self.image = self.game.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)
        else:
            self.image = self.game.terrain_spritesheet.get_sprite(0, 96, self.width, self.height)

        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

class Kenny(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.villagers
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = PLAYER_WIDTH
        self.height =  PLAYER_HEIGHT

        self.image = self.game.villager_spritesheet.get_sprite(32, 0, SPRITESHEET_WIDTH, SPRITESHEET_HEIGTH*1.5)
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 



class Enemy(Player):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = NPC_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = PLAYER_WIDTH
        self.height =  PLAYER_HEIGHT

        self.x_change = 0
        self.y_change = 0

        self.facing = 'right'
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = (100)

        self.image = self.game.enemy_spritesheet.get_sprite(0, 0, SPRITESHEET_WIDTH, SPRITESHEET_HEIGTH)
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 


    def update(self):
        
        self.movement()
        self.animation()
        
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):

        global distance_x
        global distance_y
        distance_x = 100 - self.x
        distance_y = 100 - self.y
        distance_player = (distance_x ** 2 + distance_y ** 2) ** 0.5
        distance_base = (distance_x ** 2 + distance_y ** 2) **0.5

        if distance_player < 100:      
            if distance_player != 0:
                self.rect.x += ENEMY_HUNTING_SPEED * distance_x / distance_player
                self.rect.y += ENEMY_HUNTING_SPEED * distance_y / distance_player
        else:
            self.rect.x += ENEMY_SPEED * distance_x / distance_base
            self.rect.x += ENEMY_SPEED * distance_x / distance_base  



        #if self.facing == 'left':
        #    self.x_change -= ENEMY_SPEED
        #    self.movement_loop -= 1
        #    if self.movement_loop <= -self.max_travel:
        #        self.facing = 'right'

        #if self.facing == 'right':
        #    self.x_change += ENEMY_SPEED
        #    print (self.x_change)
        #    self.movement_loop += 1
        #    if self.movement_loop >= self.max_travel:
        #        self.facing = 'left'


    def animation(self):
        
        left_animation = [(self.game.enemy_spritesheet.get_sprite(0, 0, 32, 32)), (self.game.enemy_spritesheet.get_sprite(32, 0, 32, 32)), (self.game.enemy_spritesheet.get_sprite(64, 0, 32, 32))]
        right_animation = [(self.game.enemy_spritesheet.get_sprite(64, 32, 32, 32)), (self.game.enemy_spritesheet.get_sprite(32, 32, 32, 32)), (self.game.enemy_spritesheet.get_sprite(0, 32, 32, 32))]

        if distance_x > 0:
            self.image = left_animation[math.floor(self.animation_loop)]
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.animation_loop += 0.05
            if self.animation_loop >= 3:
                self.animation_loop = 1

        if distance_x < 0:
            self.image = right_animation[math.floor(self.animation_loop)]
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.animation_loop += 0.05
            if self.animation_loop >= 3:
                self.animation_loop = 1
