#imports
import pygame
from pygame.locals import *
import sys

#init 2d game
pygame.init()

#game vars
HEIGHT = 900
WIDTH  = 1600
FPS    = 60
FONT   = pygame.font.SysFont('Congenial', 50)

#business vars

#player vars
MONEY        = 100
STOCK_QUANTS = [0,0,0,0,0]

#set up fps
FramePerSec = pygame.time.Clock()

#set up window
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

#ui
elements = []

class panel(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int, color: tuple, label: str, label_pos: tuple):
        super().__init__()
        self.pos   = (x, y)
        self.surf  = pygame.Surface((w, h))
        self.surf.fill(color)
        self.rect  = self.surf.get_rect(center = (x + w/2, y + h/2))
        self.label = FONT.render(label, True, (0, 0, 0))
        self.surf.blit(self.label, label_pos)
        elements.append(self)

#incremental panel
inc_panel   = panel(0          , 0           , 400, 900, (150, 150, 150), 'Businesses'    , (50, 50))
event_panel = panel(WIDTH - 400, HEIGHT - 200, 400, 200, (100, 100, 100), 'Current Event:', (25, 25)) 

#draw ui elements
def draw_ui():
    for element in elements:
        displaysurface.blit(element.surf, element.rect)

#game loop
while True:
    for event in pygame.event.get():
        #escape
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #update screen
    #bg
    displaysurface.fill((230, 230, 230))
    #elements
    draw_ui()

    pygame.display.update()
    FramePerSec.tick(FPS)