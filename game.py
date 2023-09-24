#imports
import pygame
from pygame.locals import *
import sys
import random as r

#init 2d game
pygame.init()

#window vars
HEIGHT = 900
WIDTH  = 1600
FPS    = 60

#text setup
FONT   = pygame.font.SysFont('Congenial', 50)

#time related vars
TICK   = 0 #1/FPS of a second, used to determine a second
TIME   = 0 #seconds since start

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
    def __init__(self, name: str, init_val: int, chng_amt: int):
        self.type       = name       #name of stock
        self.val        = init_val   #initial value 
        self.inc_chance = 50         #chance of incrementing positively (edited by events)
        self.chng_amt   = chng_amt   #maximum amount to change by either up or down (also edited by events)
        stocks.append(self)

    def update(self):
        if r.randint(1, 100) <= self.inc_chance:
            self.val += r.randint(0, self.chng_amt)
        else:
            self.val -= r.randint(0, self.chng_amt)

forest_stock = stock('GameStop', 10, 1)

#events
events = []

class event():
    def __init__(self, targets: list, name: str, desc: str, duration: int):
        self.target = targets   #types of stock to target
        self.name   = name      #name of event to be displayed
        self.desc   = desc      #description to be displayed
        self.dur    = duration  #in seconds, how long the event lasts

    def trigger(self, old_inc: int, new_inc: int, old_chng: int, new_chng: int, start_time: int):
        self.old_inc  = old_inc  #save original stock incrememnt chance to reset after event
        self.new_inc  = new_inc  #new chance to increment up
        self.old_chng = old_chng #save old increment amount to reset after event
        self.new_chng = new_chng #new increment amount

#ui
elements = []

class panel(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int, color: tuple, label: str, label_pos: tuple):
        super().__init__()
        self.pos   = (x, y)                                          #position of top left corner of panel on screen, starts in top left
        self.surf  = pygame.Surface((w, h))                          #creates surface to be drawn to of width w and height h
        self.surf.fill(color)                                        #fills in surface with color
        self.label = FONT.render(label, True, (0, 0, 0))             #creates label for the panel
        self.surf.blit(self.label, label_pos)                        #applies label to panel
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