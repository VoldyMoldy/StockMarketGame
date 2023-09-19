#imports
import pygame
from pygame.locals import *
import sys
import random as r

#init 2d game
pygame.init()

#game vars
HEIGHT = 900
WIDTH  = 1600
FPS    = 60
FONT   = pygame.font.SysFont('Congenial', 50)
TICK   = 0

#business vars

#player vars
MONEY        = 100
STOCK_QUANTS = [0,0,0,0,0]

#set up fps
FramePerSec = pygame.time.Clock()

#set up window
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

#stocks
stocks = []

class stock():
    def __init__(self, name: str, init_val: int, inc_chance: int, chng_amt: int):
        super.__init__()
        self.type       = name
        self.val        = init_val
        self.inc_chance = inc_chance
        self.chng_amt   = chng_amt
        stocks.append(self)

    def update(self):
        if r.randint(1, 100) <= self.inc_chance:
            self.val += r.randint(0, self.chng_amt)
        else:
            self.val -= r.randint(0, self.chng_amt)

forest_stock = stock('Forest', 10, 50, 1)

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

    #uptade tick
    TICK += 1
    #update stocks each second
    if TICK % FPS == 0:
        for stock_type in stocks:
            stock_type.update()
    #update screen
    #bg
    displaysurface.fill((230, 230, 230))
    #elements
    draw_ui()

    pygame.display.update()
    FramePerSec.tick(FPS)