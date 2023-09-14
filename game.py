#imports
import pygame
from pygame.locals import *
import sys

#init 2d game
pygame.init()
vec = pygame.math.Vector2

#game vars
HEIGHT    = 900
WIDTH     = 1600
FPS       = 60

#set up fps
FramePerSec = pygame.time.Clock()

#set up window
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

#game loop
while True:
    for event in pygame.event.get():
        #escape
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #update screen
    displaysurface.fill((0,0,0))

    pygame.display.update()
    FramePerSec.tick(FPS)