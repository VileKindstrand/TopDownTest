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
                    Trunk(self, y_pos, x_pos)
                if coloumn == "K":
                    Kenny(self, y_pos, x_pos)
                if coloumn == "E":
                    Enemy(self, y_pos, x_pos)
                if coloumn == "W":
                    Waterjug(self, y_pos, x_pos)


    def __init__(self):
        pygame.init()
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)      #skapar skärm
        self.screen = pygame.display.set_mode((900, 700))
        global screen
        screen = self.screen
        self.clock = pygame.time.Clock()
        self.running = True

        # self.ser = serial.Serial('COM3', 9600)

        
        self.water_level = FIRST_WATER_LEVEL
        self.player_hp = FIRST_PLAYER_HP

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
        self.text_box = pygame.sprite.LayeredUpdates()
        self.waterjugs = pygame.sprite.LayeredUpdates()

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
                    

    def arduino_input(self):
        # while self.playing:
            #print ("arduino_input")
            # self.arduino_data = self.ser.readline().decode("utf-8").strip()   
            # # Convert the received data to a float
            # global sensor_value
            # sensor_value = float(self.arduino_data)
            # print (sensor_value)
        pass


    def update(self):
        self.all_sprites.update()
        #print(self.player.player_true_x)



    def draw(self):
        self.screen.fill(GREEN)
        self.all_sprites.draw(self.screen)            
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
            # if self.player_hp < 0 or self.water_level < 0:
            #     self.playing = False





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