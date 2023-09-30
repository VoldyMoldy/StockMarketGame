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
FONT   = pygame.font.SysFont('Congenial', 35)

#time related vars
TICK   = 0 #1/FPS of a second, used to determine a second
TIME   = 0 #seconds since start

#business vars

#player vars
MONEY        = 100
STOCK_QUANTS = [10,10,10,10,10]

#set up fps
FramePerSec = pygame.time.Clock()

#set up window
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

#stocks
stocks = []

class stock():
    def __init__(self, name: str, init_val: int, chng_amt: float):
        self.type           = name       #name of stock
        self.val            = init_val   #initial value 
        self.inc_chance     = 50         #chance of incrementing positively (edited by events)
        self.chng_amt       = chng_amt   #maximum amount to change by either up or down (also edited by events)
        self.reset_chng_amt = chng_amt   #save increment value in case of events
        stocks.append(self)

    def update(self):
        if r.randint(1, 100) <= self.inc_chance:
            self.val += r.random() * self.chng_amt
        else:
            self.val -= r.random() * self.chng_amt
        if self.val < 0:
            self.val = 0
    
    def reset(self):
        self.inc_chance = 50
        self.chng_amt   = self.reset_chng_amt

gamestop_stock = stock('GameStop', 10, 0.2)
startup_stock  = stock('Random Startup Company', 35, 0.7) #need to change name
twitter_stock  = stock('X', 75, 3) #can change any of these next 3 to whatever if wanted, just have them be in ascending value
apple_stock    = stock('Apple', 150, 7.5)
apple_stock.inc_chance = 55 #is doing good
google_stock   = stock('Google', 500, 60)
google_stock.inc_chance  = 60 #top value stock is doing very well

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
        events.append(self)

    def trigger(self, start_time: int):
        self.start    = start_time #save start time of event to keep track of duration
        for stock in stocks:       #iterate through all stocks to find targets, replace stats for the event
            if stock.type in self.targets:
                stock.inc_chance = self.new_inc
                stock.chng_amt   = self.new_chng

    def check_end(self): #check if event is ended, if so reset changed stock stats and set current event to nothing
        global current_event
        if TIME - self.dur == self.start:
            for stock in stocks:
                if stock.type in self.targets:
                    stock.reset()
            current_event = None

wallstreet_bets = event(['GameStop'], 'Wallstreet Bets Strikes Again!', 'Of course its Gamestop...'  , 30, 80, .5)
controversy     = event(['GameStop'], 'Controversial Decision!'       , 'Way to lose your customers!', 40, 20, .3)

#ui
elements = []

class panel(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int, color: tuple, label: str, label_pos: tuple):
        super().__init__()
        self.pos   = (x, y)                                          #position of top left corner of panel on screen, starts in top left
        self.surf  = pygame.Surface((w, h))                          #creates surface to be drawn to of width w and height h
        self.color = color                                           #save color for updating
        self.surf.fill(color)                                        #fills in surface with color
        self.rect  = self.surf.get_rect(center = (x + w/2, y + h/2)) #rect to draw to on game loop
        self.label = FONT.render(label, True, (0, 0, 0))
        self.label_pos = label_pos                                   #creates label for the panel and saves pos for updating
        self.surf.blit(self.label, self.label_pos)                   #applies label to panel
        elements.append(self)

    def update_label(self, new_label: str):
        self.surf.fill(self.color)                           #clear old text by filling over it
        self.label = FONT.render(new_label, True, (0, 0, 0)) #recreate label with new text
        self.surf.blit(self.label, self.label_pos)           #draw text to surface

#business panels
inc_panel        = panel(0          , 0           , 400, 900, (150, 150, 150), 'Businesses'    , (50, 50))

#event panels
event_panel      = panel(WIDTH - 400, HEIGHT - 200, 400, 200, (100, 100, 100), 'Current Event:', (25, 25))
event_name_panel = panel(WIDTH - 400, HEIGHT - 133, 400, 133, (100, 100, 100), '',               (25, 25))
event_desc_panel = panel(WIDTH - 400, HEIGHT -  67, 400, 67 , (100, 100, 100), '',               (25, 25))

#stock panels
gamestop_name_panel = panel(400, 0          , 800, HEIGHT / 10, (230, 230, 230), 'GameStop: $' + str(gamestop_stock.val), (25, 25))
gamestop_info_panel = panel(400, HEIGHT / 10, 800, HEIGHT / 10, (230, 230, 230), 'You have ' + str(STOCK_QUANTS[0]) + ' stocks for a total of $' + str(STOCK_QUANTS[0] * gamestop_stock.val), (25, 25))

startup_name_panel = panel(400,     HEIGHT / 5 , 800, HEIGHT / 10, (230, 230, 230), 'Random Startup Company: $' + str(startup_stock.val), (25, 25))
startup_info_panel = panel(400, 3 * HEIGHT / 10, 800, HEIGHT / 10, (230, 230, 230), 'You have ' + str(STOCK_QUANTS[1]) + ' stocks for a total of $' + str(STOCK_QUANTS[1] * startup_stock.val), (25, 25))

x_name_panel = panel(400, 2 * HEIGHT / 5 , 800, HEIGHT / 10, (230, 230, 230), 'X: $' + str(gamestop_stock.val), (25, 25))
x_info_panel = panel(400, 5 * HEIGHT / 10, 800, HEIGHT / 10, (230, 230, 230), 'You have ' + str(STOCK_QUANTS[2]) + ' stocks for a total of $' + str(STOCK_QUANTS[2] * twitter_stock.val), (25, 25))

apple_name_panel = panel(400, 3 * HEIGHT / 5 , 800, HEIGHT / 10, (230, 230, 230), 'Apple: $' + str(gamestop_stock.val), (25, 25))
apple_info_panel = panel(400, 7 * HEIGHT / 10, 800, HEIGHT / 10, (230, 230, 230), 'You have ' + str(STOCK_QUANTS[3]) + ' stocks for a total of $' + str(STOCK_QUANTS[3] * apple_stock.val), (25, 25))

google_name_panel = panel(400, 4 * HEIGHT / 5 , 800, HEIGHT / 10, (230, 230, 230), 'Google: $' + str(gamestop_stock.val), (25, 25))
google_info_panel = panel(400, 9 * HEIGHT / 10, 800, HEIGHT / 10, (230, 230, 230), 'You have ' + str(STOCK_QUANTS[4]) + ' stocks for a total of $' + str(STOCK_QUANTS[4] * google_stock.val), (25, 25))

#hardcoded for now, maybe automate later
def update_panel_labels():
    gamestop_name_panel.update_label('GameStop: $' + ("%.2f" % gamestop_stock.val))
    gamestop_info_panel.update_label('You have ' + str(STOCK_QUANTS[0]) + ' stocks for a total of $' + ("%.2f" % (STOCK_QUANTS[0] * gamestop_stock.val)))

    startup_name_panel.update_label('Random Startup Company: $' + ("%.2f" % startup_stock.val))
    startup_info_panel.update_label('You have ' + str(STOCK_QUANTS[0]) + ' stocks for a total of $' + ("%.2f" % (STOCK_QUANTS[0] * startup_stock.val)))

    x_name_panel.update_label('X: $' + ("%.2f" % twitter_stock.val))
    x_info_panel.update_label('You have ' + str(STOCK_QUANTS[0]) + ' stocks for a total of $' + ("%.2f" % (STOCK_QUANTS[0] * twitter_stock.val)))

    apple_name_panel.update_label('Apple: $' + ("%.2f" % apple_stock.val))
    apple_info_panel.update_label('You have ' + str(STOCK_QUANTS[0]) + ' stocks for a total of $' + ("%.2f" % (STOCK_QUANTS[0] * apple_stock.val)))

    google_name_panel.update_label('Google: $' + ("%.2f" % google_stock.val))
    google_info_panel.update_label('You have ' + str(STOCK_QUANTS[0]) + ' stocks for a total of $' + ("%.2f" % (STOCK_QUANTS[0] * google_stock.val)))
    
    if current_event != None:
        event_name_panel.update_label(current_event.name)
        event_desc_panel.update_label(current_event.desc)
    else:
        event_name_panel.update_label('')
        event_desc_panel.update_label('')

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
    #update stocks every other second
    if TICK % (2 * FPS) == 0:
        TIME += 1
        for stock_type in stocks:
            stock_type.update()
        if current_event != None:
            current_event.check_end()
    #run event every minute except for the first
    if TICK % FPS == 0 and TIME % 60 == 0 and TIME != 0:
        current_event = events[r.randint(0, len(events) - 1)]
        current_event.trigger(TIME)
    #update screen
    #bg
    displaysurface.fill((230, 230, 230))
    #elements
    update_panel_labels()
    draw_ui()

    pygame.display.update()
    FramePerSec.tick(FPS)