from turtle import left, right, screensize
import pygame
from sprites import *
from config import *
import threading
import serial
#from data_gather import *
import sys
class Game(Spritesheet):

    def createTilemap(self):
        for x_pos, row in enumerate(tilemap):    # x_pos = tile-x_position  row = tile_värde   for loopen går igenom en rad
            for y_pos, coloumn in enumerate(row):    # y_pos = tile-y_position  går ner till nästa rad (och går tillbaka till första for loop?)

                Ground(self, y_pos, x_pos)
                if coloumn == "B":
                    Block(self, y_pos, x_pos)
                if coloumn == "P":
                    self.player = Player(self, y_pos, x_pos)
                if coloumn == "T":
                    self.trunk = Trunk(self, y_pos, x_pos)
                    self.trunk_list.append(self.trunk)
                if coloumn == "K":
                    Kenny(self, y_pos, x_pos)
                if coloumn == "E":
                    self.enemy = Enemy(self, y_pos, x_pos)
                if coloumn == "W":
                    self.waterjug = Waterjug(self, y_pos, x_pos)
        self.textbox = Textbox(self, y_pos, x_pos)


    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)      #skapar skärm
        #self.screen = pygame.display.set_mode((900, 700))
        global screen
        screen = self.screen
        self.clock = pygame.time.Clock()
        self.running = True

        # self.ser = serial.Serial('COM3', 9600)

        
        self.water_level = FIRST_WATER_LEVEL
        self.player_hp = FIRST_PLAYER_HP
        self.trunk_list = []

        self.character_spritesheet = Spritesheet("img/gecko_spritesheet.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.villager_spritesheet = Spritesheet("img/villager_spritesheet.png")
        self.enemy_spritesheet = Spritesheet("img/enemy_spritesheet.png")

    def new(self):
        #nytt spel startar
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.villagers = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.trunks = pygame.sprite.LayeredUpdates()
        self.waterjugs = pygame.sprite.LayeredUpdates()
        self.textboxes = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - PROJECTILE_WIDTH, self.player.rect.y + PLAYER_HEIGHT / 2)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + PLAYER_WIDTH, self.player.rect.y + PLAYER_HEIGHT / 2) 
                if event.key == pygame.K_TAB:
                    Textbox(self, 1, 1) 
                    # print (random.randint(1, len(self.trunks)))
                    # Enemy(self, self.trunk_list[random.randint(0, len(self.trunks) - 1)].rect.x / TILESIZE, self.trunk_list[random.randint(0, len(self.trunks) - 1)].rect.y / TILESIZE) 
                    

    def arduino_input(self):
        # while self.playing:
            #print ("arduino_input")
            # self.arduino_data = self.ser.readline().decode("utf-8").strip()   
            # # Convert the received data to a float
            # self.sensor_value
            # sensor_value = float(self.arduino_data)
            # self.water_level -= 10
        pass

    def random_spawn(self):
        if FPS * int(self.water_level / 20) > 1:
            self.spawn_rate = random.randint(1, FPS * int(self.water_level / 20))  
        else:
            self.spawn_rate = random.randint(1, FPS * int(FIRST_WATER_LEVEL * SPAWN_RATE))
        if self.spawn_rate == 10:
            self.random_trunk = self.trunk_list[random.randint(0, len(self.trunks) - 1)]
            Enemy(self, self.random_trunk.rect.x / TILESIZE, self.random_trunk.rect.y / TILESIZE) 
            # Enemy(self, self.trunk_list[random.randint(0, len(self.trunks) - 1)].rect.x / TILESIZE, self.trunk_list[random.randint(0, len(self.trunks) - 1)].rect.y / TILESIZE) 

    def update(self):
        self.all_sprites.update()
        self.random_spawn()
        self.textboxes.update()
        #print(self.player.player_true_x)



    def draw(self):
        self.screen.fill(GREEN)
        self.all_sprites.draw(self.screen)      
        self.textboxes.draw(self.screen)     
        self.screen.blit(self.textbox.water_level_blit, (TILESIZE/16, 0)) 
        self.screen.blit(self.textbox.player_level_blit, (TILESIZE/16, TILESIZE))
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #game loop
        self.data_gather = threading.Thread(target=g.arduino_input, args=())
        self.data_gather.start()
        while self.playing:                             
            self.events()       #kollar efter input
            self.update()       #uppdaterar skärm
            self.draw()       #pyntar skiten
            if self.player_hp < 0 or self.water_level < 0:
                self.playing = False





        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        pass

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()