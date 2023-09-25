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
        self.type           = name       #name of stock
        self.val            = init_val   #initial value 
        self.inc_chance     = 50         #chance of incrementing positively (edited by events)
        self.chng_amt       = chng_amt   #maximum amount to change by either up or down (also edited by events)
        self.reset_chng_amt = chng_amt   #save increment value in case of events
        stocks.append(self)

    def update(self):
        if r.randint(1, 100) <= self.inc_chance:
            self.val += r.randint(0, self.chng_amt)
        else:
            self.val -= r.randint(0, self.chng_amt)
    
    def reset(self):
        self.inc_chance = 50
        self.chng_amt   = self.reset_chng_amt

gamestop_stock = stock('GameStop', 10, 1)

#events
events = []
current_event = None

class event():
    def __init__(self, targets: list, name: str, desc: str, duration: int, new_inc: int, new_chng: int):
        self.targets  = targets  #types of stock to target
        self.name     = name     #name of event to be displayed
        self.desc     = desc     #description to be displayed
        self.dur      = duration #in seconds, how long the event lasts
        self.new_inc  = new_inc  #new chance to increment up
        self.new_chng = new_chng #new increment amount

    def trigger(self, start_time: int):
        self.start    = start_time #save start time of event to keep track of duration
        for stock in stocks:       #iterate through all stocks to find targets, replace stats for the event
            if stock.type in self.targets:
                stock.inc_chance = self.new_inc
                stock.chng_amt   = self.new_chng

    def check_end(self): #check if event is ended, if so reset changed stock stats and set current event to nothing
        if TIME - self.dur == self.start:
            for stock in stocks:
                if stock.type in self.targets:
                    stock.reset()
            current_event = None

wallstreet_bets = event(['Gamestop'], 'Wallstreet Bets Strikes Again!', 'Of course it\'s Gamestop...', 30, 4, 80)

#ui
elements = []

class panel(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int, color: tuple, label: str, label_pos: tuple):
        super().__init__()
        self.pos   = (x, y)                                          #position of top left corner of panel on screen, starts in top left
        self.surf  = pygame.Surface((w, h))                          #creates surface to be drawn to of width w and height h
        self.surf.fill(color)                                        #fills in surface with color
        self.rect  = self.surf.get_rect(center = (x + w/2, y + h/2)) #rect to draw to on game loop
        self.label = FONT.render(label, True, (0, 0, 0))             #creates label for the panel
        self.surf.blit(self.label, label_pos)                        #applies label to panel
        elements.append(self)

inc_panel   = panel(0          , 0           , 400, 900, (150, 150, 150), 'Businesses'            , (50, 50))
event_panel = panel(WIDTH - 400, HEIGHT - 200, 400, 200, (100, 100, 100), 'Current Event:\nNothing', (25, 25))

if current_event != None:
    event_panel.label = 'Current Event:\n' + current_event.name + '\n' + current_event.desc

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
        TIME += 1
        for stock_type in stocks:
            stock_type.update()
        if current_event != None:
            current_event.check_end()
    #run event every minute except for the first
    if TIME != 0 and TIME % 60 == 0:
        current_event = events[r.randint(0, len(events) - 1)]
        current_event.trigger(TIME)
    #update screen
    #bg
    displaysurface.fill((230, 230, 230))
    #elements
    draw_ui()

    pygame.display.update()
    FramePerSec.tick(FPS)