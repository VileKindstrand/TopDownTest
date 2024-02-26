from distutils.spawn import spawn
from turtle import left, right, screensize
import pygame
#from data_gather import arduino_input
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
        self.screen_x, self.screen_y = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.small_font = pygame.font.SysFont('Comic Sans MS', 15)
        self.running = True

        self.ser = serial.Serial('COM3', 9600)

        
        self.water_level = FIRST_WATER_LEVEL
        self.player_hp = FIRST_PLAYER_HP
        self.trunk_list = []

        self.character_spritesheet = Spritesheet("img/gecko_spritesheet.png")
        self.terrain_spritesheet = Spritesheet("img/terrain.png")
        self.villager_spritesheet = Spritesheet("img/villager_spritesheet.png")
        self.enemy_spritesheet = Spritesheet("img/enemy_spritesheet.png")
        self.intro_background = pygame.image.load('./img/intro_img.jpg')
        self.intro_background = pygame.transform.scale(self.intro_background, (self.screen_x, self.screen_y))

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

        for sprite in self.all_sprites:
            sprite.rect.x -= self.player.rect.x - self.screen_x / 2
            sprite.rect.y -= self.player.rect.y - self.screen_y / 2

        self.water_level = FIRST_WATER_LEVEL
        self.player_hp = FIRST_PLAYER_HP
        self.data_gather = threading.Thread(target=g.arduino_input, args=())
        self.data_gather.start()

    def events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            if self.player_hp > 3:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.player.facing == 'left':
                            Attack(self, self.player.rect.x - PROJECTILE_WIDTH, self.player.rect.y + PLAYER_HEIGHT / 2)
                        if self.player.facing == 'right':
                            Attack(self, self.player.rect.x + PLAYER_WIDTH, self.player.rect.y + PLAYER_HEIGHT / 2) 
                # if event.key == pygame.K_TAB:
                #     Textbox(self, 1, 1) 
                    # print (random.randint(1, len(self.trunks)))
                    # Enemy(self, self.trunk_list[random.randint(0, len(self.trunks) - 1)].rect.x / TILESIZE, self.trunk_list[random.randint(0, len(self.trunks) - 1)].rect.y / TILESIZE) 
                    

    def arduino_input(self):
        while self.playing:
            self.arduino_data = self.ser.readline().decode("utf-8").strip()   
            # Convert the received data to a float
            sensor_value = float(self.arduino_data)
            self.water_level -= sensor_value * 10
    

    def random_spawn(self):
        if FPS * int(self.water_level / SPAWN_RATE) > 1:
            self.spawn_rate = random.randint(1, FPS * int(self.water_level / SPAWN_RATE))  
        else:
            self.spawn_rate = random.randint(1, FPS * int(FIRST_WATER_LEVEL / SPAWN_RATE / 4))
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
        self.screen.blit(self.textbox.score_level_blit, (TILESIZE/16, 2 * TILESIZE))
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #game loop
        while self.playing:                             
            self.events()       #kollar efter input
            self.update()       #uppdaterar skärm
            self.draw()       #pyntar skiten
            if self.player_hp < 0 or self.water_level < 0:
                self.playing = False





        self.running = False

    def game_over(self):
        pass
    #     self.running = True

    #     print ("inne")

    #     title = self.font.render('Operation paper pal: The Game', True, BLACK)
    #     title_rect = title.get_rect(x=10, y=10)
    #     restart_button = Startbutton(Game, 10, 50, 200, 50, BLACK, GREEN, 'Play', 32)
    #     info_text_pt1 = "Did you know that a single piece of toiletpaper costs almost a Litre of water to make?"
    #     info_text_pt2 = "For how long can you survive in Little Gecko's world before you and the enviornment dries to death?"
    #     info_pt1 = self.small_font.render(info_text_pt1, True, BLACK)
    #     info_pt1_rect = title.get_rect(x = 10, y = 120)
    #     info_pt2 = self.small_font.render(info_text_pt2, True, BLACK)
    #     info_pt2_rect = title.get_rect(x = 10, y = 140)

    #     for sprite in self.all_sprites:
    #         sprite.kill()

    #     while self.running:

    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 outro = False
                    

    #         mouse_pos = pygame.mouse.get_pos()
    #         mouse_pressed = pygame.mouse.get_pressed()

    #         if restart_button.is_pressed(mouse_pos, mouse_pressed):
    #             self.playing = True
    #             self.running = True
    #             print ("if")
    #             self.new()
    #             print("new")
    #             self.main()
    #             print(self.running)
    #             print (self.playing)

    #         # score_text = self.small_font.render(self.textbox.score_count, True, BLACK)
    #         # score_text_rect = title.get_rect(x = 10, y = 120)

    #         self.screen.blit(self.intro_background, (0, 0))  # Draw the background image first
    #         self.screen.blit(title, title_rect)
    #         self.screen.blit(restart_button.image, restart_button.rect)
    #         self.screen.blit(info_pt1, info_pt1_rect)
    #         self.screen.blit(info_pt2, info_pt2_rect)
    #         pygame.display.flip()  # Update the entire screen
    #         self.clock.tick(FPS)

    def intro_screen(self):
        intro = True


        title = self.font.render('Operation paper pal: The Game', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)
        play_button = Startbutton(Game, 10, 50, 200, 50, BLACK, GREEN, 'Play', 32)
        info_text_pt1 = "Did you know that a single piece of toiletpaper costs almost a Litre of water to make?"
        info_text_pt2 = "For how long can you survive in Little Gecko's world before you and the enviornment dries to death?"
        info_pt1 = self.small_font.render(info_text_pt1, True, BLACK)
        info_pt1_rect = title.get_rect(x = 10, y = 120)
        info_pt2 = self.small_font.render(info_text_pt2, True, BLACK)
        info_pt2_rect = title.get_rect(x = 10, y = 140)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    # self.running = True

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0, 0))  # Draw the background image first
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(info_pt1, info_pt1_rect)
            self.screen.blit(info_pt2, info_pt2_rect)
            pygame.display.flip()  # Update the entire screen
            self.clock.tick(FPS)

        # title = self.font.render('Hello world', True, BLACK)
        # title_rect = title.get_rect(x= 10 , y = 10)
        # play_button = Startbutton(Game, 10, 50, 200, 50, WHITE, WHITE, 'Play', 32)

        # while intro:
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             intro = False
        #             self.running = True

        #     mouse_pos = pygame.mouse.get_pos()
        #     mouse_pressed = pygame.mouse.get_pressed()

        #     if play_button.is_pressed(mouse_pos, mouse_pressed):
        #         intro = False

        #     self.screen.blit(self.intro_background, (0, 0))
        #     self.screen.blit(title, title_rect)
        #     self.screen.blit(play_button.image, play_button.rect)
        #     self.clock.tick(FPS)


g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()