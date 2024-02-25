import string
from tkinter import FIRST
from turtle import delay, distance
import pygame
from config import *
import math
import random




class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))       #JÄVLIGASTE FELET JAG VARIT MED OM: HADE RÅKAT SKRIVA (1,0) VILKET FÖRFLYTTADE ALLA SPRITES MED EN X PIXEL
        sprite.set_colorkey(BLACK)
        return sprite

class Textbox(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = TEXT_BOX_LAYER
        self.groups = self.game.textboxes
        pygame.sprite.Sprite.__init__(self, self.groups)

        pygame.font.init()

        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)


        self.x = x * TILESIZE
        self.y = y  * TILESIZE
        self.width = PLAYER_WIDTH
        self.height =  PLAYER_HEIGHT

        self.image = self.game.villager_spritesheet.get_sprite(32, 0, SPRITESHEET_WIDTH, SPRITESHEET_HEIGTH*1.5)
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

        print (self.rect.x, self.rect.y)
    def update(self):
        self.text()

    def text(self):

        self.water_index = str(int(self.game.water_level))
        self.player_index = str(int(self.game.player_hp))

        self.water_level_blit = self.my_font.render("water level: " + self.water_index, False, (255, 255, 255))
        self.player_level_blit = self.my_font.render("moist meter: " + self.player_index, False, (255, 255, 255))



class Waterjug(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        # self.x = x * TILESIZE * 4
        # self.y = y * TILESIZE * 2
        # self.width = SPRITESHEET_WIDTH
        # self.height =  SPRITESHEET_HEIGTH

        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.waterjugs
        pygame.sprite.Sprite.__init__(self, self.groups)


        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = SPRITESHEET_WIDTH
        self.height =  SPRITESHEET_WIDTH

        self.image = self.game.terrain_spritesheet.get_sprite(0, 32, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

    def update(self):
        pass
        #self.status()

    # def status(self):
    #     if self.game.water_level < 50:
    #         self.image = self.game.terrain_spritesheet.get_sprite(0, 32, self.width, self.height)
    #         self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
    #     else:
    #             self.image = self.game.terrain_spritesheet.get_sprite(0, 64, self.width, self.height)
    #             self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))






class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE*1.5

        global player_true_x, player_true_y
        self.player_true_x = self.x
        self.player_true_y = self.y

        self.x_change = 0
        self.y_change = 0

        self.animation_loop = 1  
        self.facing = 'right'    

        #spelarens utseende
        self.image = self.game.character_spritesheet.get_sprite(33, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        


    def update(self):

        self.movement()
        self.animation()
        self.interact_villagers()
        self.interact_enemies()
        self.interact_waterjug()

        self.rect.x += self.x_change         # VID DIAGONAL LINJE RÖR MAN SIG SNABBARE; FIXA "NORMALIZED VECTOR". Vet dock inte hur det här fungerar än
        self.player_true_x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.player_true_y += self.x_change
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

        if keys[pygame.K_w] and keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED / (2 ** 0.5)
                sprite.rect.y += PLAYER_SPEED / (2 ** 0.5)
            self.y_change -= PLAYER_SPEED / (2 ** 0.5)
            self.x_change  -= PLAYER_SPEED / (2 ** 0.5)
            self.facing = 'left'
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED / (2 ** 0.5)
                sprite.rect.y += PLAYER_SPEED / (2 ** 0.5)
            self.y_change -= PLAYER_SPEED / (2 ** 0.5)
            self.x_change  += PLAYER_SPEED / (2 ** 0.5)
            self.facing = 'right'
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED / (2 ** 0.5)
                sprite.rect.y -= PLAYER_SPEED / (2 ** 0.5)
            self.y_change += PLAYER_SPEED / (2 ** 0.5)
            self.x_change  -= PLAYER_SPEED / (2 ** 0.5)
            self.facing = 'left'
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED / (2 ** 0.5)
                sprite.rect.y -= PLAYER_SPEED / (2 ** 0.5)
            self.y_change += PLAYER_SPEED / (2 ** 0.5)
            self.x_change += PLAYER_SPEED / (2 ** 0.5)
            self.facing = 'right'
        elif keys[pygame.K_a]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change  -= PLAYER_SPEED
            self.facing = 'left'
        elif keys[pygame.K_d]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        elif keys[pygame.K_w]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
        elif keys[pygame.K_s]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
        global y_change
        global x_change
        y_change = self.y_change
        x_change = self.x_change
            #self.facing = 'down'



    def interact_waterjug(self):
        hits = pygame.sprite.spritecollide(self, self.game.waterjugs, False)
        keys = pygame.key.get_pressed()
        if hits:
            if keys[pygame.K_LCTRL]:
                if self.game.player_hp < FIRST_PLAYER_HP:
                    self.game.water_level -= WATER_EXCHANGE
                    self.game.player_hp += WATER_EXCHANGE
                    print(self.game.water_level, self.game.player_hp)

    def interact_villagers(self):
        #screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
        hits = pygame.sprite.spritecollide(self, self.game.villagers, False)
        keys = pygame.key.get_pressed()
        if hits:
            if keys[pygame.K_LCTRL]:
                self.game.water_level += 1
                print(self.game.water_level)

    def interact_enemies(self):
        #screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
        self.dialogue_box = False

        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
                self.game.player_hp -= ENEMY_DAMAGE
                print(self.game.player_hp)



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
        
        left_animation = [self.game.villager_spritesheet.get_sprite(1, 0, self.width, self.height),          #degposition
                          self.game.character_spritesheet.get_sprite(34, 0, SPRITESHEET_WIDTH, SPRITESHEET_HEIGTH*1.5),         #låg hopp
                          self.game.character_spritesheet.get_sprite(67, 0, SPRITESHEET_WIDTH, SPRITESHEET_HEIGTH*1.5)]      #hög hopp

        right_animation = [self.game.character_spritesheet.get_sprite(67, 48, self.width, self.height),
                          self.game.character_spritesheet.get_sprite(34, 48, SPRITESHEET_WIDTH, SPRITESHEET_HEIGTH*1.5),         
                          self.game.character_spritesheet.get_sprite(1, 48, SPRITESHEET_WIDTH, SPRITESHEET_HEIGTH*1.5)]

        if self.facing == "left":
            self.old_facing = self.facing
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 0, SPRITESHEET_WIDTH, SPRITESHEET_HEIGTH*1.5)
                self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
            else:
                self.image = left_animation[math.floor(self.animation_loop)]
                self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                self.animation_loop += 0.05
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(67, 48, SPRITESHEET_WIDTH, SPRITESHEET_HEIGTH*1.5)
                self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
            else:
                self.image = right_animation[math.floor(self.animation_loop)]
                self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                self.animation_loop += 0.05
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        # if self.facing == "up":
        #     if self.x_change == 0:
        #         self.image = self.game.character_spritesheet.get_sprite(1, 0, self.width, 48)
        #         self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        #     else:
        #         self.image = left_animation[math.floor(self.animation_loop)]
        #         self.animation_loop += 0.05
        #         if self.animation_loop >= 3:
        #             self.animation_loop = 1
        # if self.facing == "down":
        #     if self.x_change == 0:
        #         self.image = self.game.character_spritesheet.get_sprite(1, 0, self.width, 48)
        #         self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        #     else:
        #         self.image = left_animation[math.floor(self.animation_loop)]
        #         self.animation_loop += 0.05
        #         if self.animation_loop >= 3:
        #             self.animation_loop = 1





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

        self.image = self.game.terrain_spritesheet.get_sprite(0, 32, 32, 32)
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

class Trunk(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites, self.game.trunks
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

    def update(self):
        pass

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

        self.image = self.game.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

        if self.game.water_level > 50:
            self.image = self.game.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)
            self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        else:
            self.image = self.game.terrain_spritesheet.get_sprite(0, 128, self.width, self.height)
            self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

    def update(self):
        self.animation()

    def animation(self):
        if self.game.water_level > FIRST_WATER_LEVEL / 2:
            self.image = self.game.terrain_spritesheet.get_sprite(0, 0, self.width, self.height)
            self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        else:
            self.image = self.game.terrain_spritesheet.get_sprite(0, 96, self.width, self.height)
            self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))

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
        self.enemy_true_x = self.x
        self.enemy_true_y = self.y


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
        self.collision_blocks()
        
        self.rect.x += self.x_change
        self.enemy_true_x += self.x_change
        self.rect.y += self.y_change
        self.enemy_true_y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):

        self.distance_x = self.game.waterjug.rect.x - self.rect.x
        self.distance_y = self.game.waterjug.rect.y - self.rect.y
        self.distance = (self.distance_x ** 2 +self.distance_y ** 2) ** 0.5


        if distance != 0:
            if self.game.water_level > FIRST_WATER_LEVEL / 2:
                self.x_change += ENEMY_SPEED * self.distance_x / self.distance
                self.y_change += ENEMY_SPEED * self.distance_y / self.distance
            else:
                self.x_change += ENEMY_DRY_SPEED * self.distance_x / self.distance
                self.y_change += ENEMY_DRY_SPEED * self.distance_y / self.distance

            # self.enemy_true_x += ENEMY_SPEED * self.distance_x / self.distance
            # self.rect.x += ENEMY_SPEED * self.distance_x / self.distance
            # self.enemy_true_y += ENEMY_SPEED * self.distance_y / self.distance
            # self.rect.y += ENEMY_SPEED * self.distance_y / self.distance

        # self.distance_x = self.game.player.player_true_x - self.enemy_true_x
        # self.distance_y = self.game.player.player_true_y - self.enemy_true_y
        # self.distance_player = (self.distance_x ** 2 + self.distance_y ** 2) ** 0.5
        # self.distance_base = (self.distance_x ** 2 + self.distance_y ** 2) **0.5
        # print (self.game.player.player_true_x, self.enemy_true_x)
        # print (self.game.player.player_true_y, self.enemy_true_y)

        # if distance_player < 100:      
        #     if distance_player != 0:
        # self.x_change += ENEMY_SPEED * self.distance_x / self.distance_player
        # self.enemy_true_x += ENEMY_SPEED * self.distance_x / self.distance_player
        # self.y_change += ENEMY_SPEED * self.distance_y / self.distance_player
        # self.enemy_true_y += ENEMY_SPEED * self.distance_y / self.distance_player

        # print (self.distance_x, self.distance_y)
        # else:
        #     self.rect.x += ENEMY_SPEED * distance_x / distance_base
        #     self.rect.x += ENEMY_SPEED * distance_x / distance_base  

# # ANNAT MOVEMENT SYSTEM

#         if self.facing == 'left':
#            self.x_change -= ENEMY_SPEED
#            self.movement_loop -= 1
#            if self.movement_loop <= -self.max_travel:
#                self.facing = 'right'

#         if self.facing == 'right':
#            self.x_change += ENEMY_SPEED
#            self.movement_loop += 1
#            if self.movement_loop >= self.max_travel:
#                self.facing = 'left'

    def collision_blocks(self):
        hits = pygame.sprite.spritecollide(self, self.game.waterjugs, False)
        if hits:
            self.game.water_level -= 0.05
            print(self.game.water_level)
            self.x_change = 0
            self.y_change = 0
            


    def animation(self):
        
        left_animation = [(self.game.enemy_spritesheet.get_sprite(0, 0, 32, 32)), (self.game.enemy_spritesheet.get_sprite(32, 0, 32, 32)), (self.game.enemy_spritesheet.get_sprite(64, 0, 32, 32))]
        right_animation = [(self.game.enemy_spritesheet.get_sprite(64, 32, 32, 32)), (self.game.enemy_spritesheet.get_sprite(32, 32, 32, 32)), (self.game.enemy_spritesheet.get_sprite(0, 32, 32, 32))]
        left_dry_animation = [(self.game.enemy_spritesheet.get_sprite(0, 64, 32, 32)), (self.game.enemy_spritesheet.get_sprite(32, 64, 32, 32)), (self.game.enemy_spritesheet.get_sprite(64, 64, 32, 32))]
        right_dry_animation = [(self.game.enemy_spritesheet.get_sprite(64, 96, 32, 32)), (self.game.enemy_spritesheet.get_sprite(32, 96, 32, 32)), (self.game.enemy_spritesheet.get_sprite(0, 96, 32, 32))]

        if self.distance_x > 0:
            if self.game.water_level > FIRST_WATER_LEVEL / 2:
                self.image = left_animation[math.floor(self.animation_loop)]
                self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                self.animation_loop += 0.05
            else:
                self.image = left_dry_animation[math.floor(self.animation_loop)]
                self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                self.animation_loop += 0.05
            if self.animation_loop >= 3:
                self.animation_loop = 1

        if self.distance_x <= 0:
            if self.game.water_level > FIRST_WATER_LEVEL / 2:
                self.image = right_animation[math.floor(self.animation_loop)]
                self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
                self.animation_loop += 0.05
            else:
                self.image = right_dry_animation[math.floor(self.animation_loop)]
                self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.animation_loop += 0.05
            if self.animation_loop >= 3:
                self.animation_loop = 1


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x 
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.facing = self.game.player.facing
        self.game.player_hp -= ATTACK_COST
        print (self.game.player_hp)

        self.animation_loop = 0
        self.image = self.game.enemy_spritesheet.get_sprite(32, 0, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (PROJECTILE_WIDTH, PROJECTILE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animation()
        self.collide()
        self.velocity()
        
        #print(self.rect.x)
        #print (self.game.all_sprites)


    def velocity(self):
        pass
        if self.facing == 'right':
            self.rect.x += PROJECTILE_SPEED
        if self.facing == 'left':
            self.rect.x -= PROJECTILE_SPEED
        if self.facing == 'down':
            self.rect.y += PROJECTILE_SPEED
        if self.facing == 'up':
            self.rect.y -= PROJECTILE_SPEED


    def collide(self):
        hits_enemy = pygame.sprite.spritecollide(self, self.game.enemies, True)
        hits_block = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits_block or hits_enemy:
            self.kill()

    def animation(self):
        # print ("animation")
        direction = self.game.player.facing

        right_animation = [(self.game.enemy_spritesheet.get_sprite(0, 0, 32, 32)), (self.game.enemy_spritesheet.get_sprite(32, 0, 32, 32)), (self.game.enemy_spritesheet.get_sprite(64, 0, 32, 32))]
        left_animation = [(self.game.enemy_spritesheet.get_sprite(64, 32, 32, 32)), (self.game.enemy_spritesheet.get_sprite(32, 32, 32, 32)), (self.game.enemy_spritesheet.get_sprite(0, 32, 32, 32))]

        if direction == 'left':
            self.image = left_animation[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                # self.kill()
                self.animation_loop = 0

        if direction == 'right':
            self.image = right_animation[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 3:
                #self.kill()
                self.animation_loop = 0


