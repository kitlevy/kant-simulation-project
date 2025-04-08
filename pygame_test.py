import pygame
import pygame.freetype
import numpy as np
import os, sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Kantian Ethics Simulation"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_PATH = os.path.join(BASE_DIR, "assets")

pond_size = 50

white = (255,255,255)
blue = (173,216,230)
red = (255,0,59)
black = (0,0,0)

title_mode = True
intro_mode = False
play_mode = False

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
font = pygame.freetype.Font("assets/calibri-bold.ttf", 36)

def load_image(name):
    fullname = os.path.join(ASSET_PATH, name)
    image = pygame.image.load(fullname)
    image = image.convert()
    return image

class Game():
    def __init__(self):


class Pond:
    def __init__(self,loc,fish):
        self.fish = fish
        self.center = loc
        self.x = self.center[0]
        self.y = self.center[1]
                
    def display(self):
        pygame.draw.circle(screen,blue,self.center,pond_size)
        font.render_to(screen,(self.x-7,self.y-8),str(self.fish),black)

    def set_fish(self,num):
        self.fish += num

    def repopulate(self):
        set_fish(self.fish // 2)


running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    screen.fill(white)
    P = Pond((400,300),3)
    P.display()

    #constantly updating
    pygame.display.flip()

    pygame.time.Clock().tick(100)

pygame.quit()

