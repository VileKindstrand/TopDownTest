from turtle import left, right
import pygame
from sprites import *
from config import *
#from data_gather import *
import sys
class Game:

    def createTilemap(self):
        for x_pos, row in enumerate(tilemap):    # x_pos = tile-x_position  row = tile_värde   for loopen går igenom en rad
            for y_pos, coloumn in enumerate(row):    # y_pos = tile-y_position  går ner till nästa rad (och går tillbaka till första for loop?)

                Ground(self, y_pos, x_pos)
                if coloumn == "B":
                    Block(self, y_pos, x_pos)
                if coloumn == "P":
                    Player(self, y_pos, x_pos)
                if coloumn == "T":
                    Trunk(self, y_pos, x_pos)
                if coloumn == "K":
                    Kenny(self, y_pos, x_pos)


    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)      #skapar skärm
        self.clock = pygame.time.Clock()
        self.running = True

        self.character_spritesheet = Spritesheet("img/gecko_spritesheet.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.villager_spritesheet = Spritesheet("img/villager_spritesheet.png")


    def new(self):
        #nytt spel startar
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.villagers = pygame.sprite.LayeredUpdates()
        self.threaten = pygame.sprite.LayeredUpdates()

        self.createTilemap()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False

    def update(self):
        self.all_sprites.update()


    def draw(self):
        self.screen.fill(GREEN)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #game loop
        while self.playing:    
            self.events()       #kollar efter input
            self.update()       #uppdaterar skärm
            self.draw()       #pyntar skiten

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