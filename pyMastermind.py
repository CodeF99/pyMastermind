import pygame, os, random
from random import randint
from pygame.locals import *
from sys import exit
pygame.init()
screen = pygame.display.set_mode((300, 400), 0, 32)
pygame.display.set_caption("PyMasterMind!")
random_color = (randint(0,255), randint(0,255), randint(0,255))
font = pygame.font.SysFont("arial", 12);
screen.fill((208,208,208))

number_of_attempts = []
attempts_list = []
all_attempts_list = {}
master_list = {}
indicator_list = {}
code_list = {}
color_list = {}
color_select = []
BOARD = []
li = []
i = 0
attempts = []
attempt_map = {}

class Button:
    def __init__(self,x,y,imagefile):
      # load in the icon that will go in the middle of the button
        self.insideimg = pygame.image.load(imagefile).convert_alpha()
        self.insiderect = self.insideimg.get_rect()
        self.ix = self.insiderect.size[0]
        self.iy = self.insiderect.size[1]

      # set up base values for the size of this button to the image inside it
        self.image = pygame.surface.Surface((self.ix+8,self.iy+8))
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

      # set button as unpressed
        self.popup()

    # draw the button in an "unpressed" state
    def popup(self):
        self.image.fill((96,96,96))
        pygame.draw.line(self.image, (224,224,224), (0,0),(self.ix+8,0) )
        pygame.draw.line(self.image, (224,224,224), (0,0),(0,self.ix+8) )
        pygame.draw.line(self.image, (224,224,224), (1,1),(self.ix+7,1) )
        pygame.draw.line(self.image, (224,224,224), (1,1),(1,self.ix+7) )
        pygame.draw.line(self.image, (224,224,224), (2,2),(self.ix+6,2) )
        pygame.draw.line(self.image, (224,224,224), (2,2),(2,self.ix+6) )
        pygame.draw.rect(self.image, (160,160,160), ((3,3),(self.ix+3,self.iy+3)) )
        # put the button icon on the button
        self.image.blit(self.insideimg,(4,4))

    # draw the button in a "pressed" state
    def press(self):
        self.image.fill((224,224,224))
        pygame.draw.line(self.image, (96,96,96), (0,0),(self.ix+8,0) )
        pygame.draw.line(self.image, (96,96,96), (0,0),(0,self.ix+8) )
        pygame.draw.line(self.image, (96,96,96), (1,1),(self.ix+7,1) )
        pygame.draw.line(self.image, (96,96,96), (1,1),(1,self.ix+7) )
        pygame.draw.line(self.image, (96,96,96), (2,2),(self.ix+6,2) )
        pygame.draw.line(self.image, (96,96,96), (2,2),(2,self.ix+6) )
        pygame.draw.rect(self.image, (160,160,160), ((3,3),(self.ix+3,self.iy+3)) )
        # put the button icon on the button
        self.image.blit(self.insideimg,(4,4))

    # this gets called if the mouse is clicked - check if the button was hit
    def clicked(self,pos):
        if (self.rect.left < pos[0] < self.rect.right) and (self.rect.top < pos[1] <  self.rect.bottom):
            return 1

def init_attempt_map():
    global li, i
    for a in range(10):
        for x in range(4):
            li.append(i)
            i+=1
            attempt_map[a] = li
        li = []

def gen_master():
    for a in range(4):
        master_list[a] = code_list[randint(0,4)]
def print_master():
    pygame.draw.rect(screen, (0,0,0), Rect(25,100,7,20))
    pygame.draw.rect(screen, (0,0,0), Rect(113,100,7,20))
    for a in range(4):
        pygame.draw.ellipse(screen, master_list[a], (a*25+25,350-(10*25),20,20))
def gen_colors():
    for a in range(6):
        code_list[a] = (randint(0,255), randint(0,255), randint(0,255))
        color_list[code_list[a]] = pygame.Rect(a*25,375,20,20)
def draw_palette():
    pygame.draw.rect(screen, (0,0,0), Rect(0,375,150,20))
    for a in range(6):
        pygame.draw.ellipse(screen, code_list[a], (a*25,375,20,20))
def check_color_selection(mouse_loc):
    global color_select
    for a in range(6):
        if color_list[code_list[a]].collidepoint(mouse_loc):
            color_select = a
def init_elli():
    screen.fill(random_color)
    for z in range(10):
        for a in range(4):
            BOARD.append(pygame.Rect(a*25+25,350-(z*25),20,20))

def tooLegit(i,all_attempts_list):
    if len(all_attempts_list) > 4 and len(all_attempts_list) % 4 == 0 and (len(attempts) == len(all_attempts_list) / 4 - 1):
        if i in attempt_map[len(all_attempts_list) / 4 - 1]:
            return True
        else:
            return False
    elif len(all_attempts_list) > 4 and len(all_attempts_list) % 4 != 0 and (len(attempts) == len(all_attempts_list) / 4):
        if i in attempt_map[len(all_attempts_list) / 4]:
            return True
        else:
            return False
    elif i in attempt_map[0] and len(attempts) == 0:
        return True
    else:
        return False
def draw_elli(attempts_list,x,all_attempts_list):
    i = -1
    screen.fill((255, 255, 255))
    draw_palette()
    tempColor = []
    for z in range(10):
        for a in range(4):
            i += 1
            if i == x:
                if (pygame.Rect(a*25+25,350-(z*25),20,20)) in attempts_list:
                    tempColor = all_attempts_list[i]
                    all_attempts_list[i] = code_list[color_select]
                    if tooLegit(i,all_attempts_list):
                        pygame.draw.ellipse(screen,code_list[color_select],(a*25+25,350-(z*25),20,20))
                    else:
                        all_attempts_list[i] = tempColor
                        pygame.draw.ellipse(screen,all_attempts_list[i],(a*25+25,350-(z*25),20,20))
                else:
                    tempColor = code_list[color_select]
                    attempts_list.append(pygame.Rect(a*25+25,350-(z*25),20,20))
                    all_attempts_list[i] = code_list[color_select]
                    if tooLegit(i,all_attempts_list):
                        pygame.draw.ellipse(screen,code_list[color_select],(a*25+25,350-(z*25),20,20))
                        all_attempts_list[i] = code_list[color_select]
                    else:
                        pygame.draw.ellipse(screen, (200,200,200), (a*25+25,350-(z*25),20,20))
                        all_attempts_list.pop(i)
                        attempts_list.remove(pygame.Rect(a*25+25,350-(z*25),20,20))
            elif x != None:
                if i in all_attempts_list:
                    pygame.draw.ellipse(screen, all_attempts_list[i],(a*25+25,350-(z*25),20,20))
                else:
                    pygame.draw.ellipse(screen, (200,200,200), (a*25+25,350-(z*25),20,20))
            else:
                pygame.draw.ellipse(screen, (200,200,200), (a*25+25,350-(z*25),20,20))
    #print_master()
def randrange(start, stop):
    values = range(start, stop)
    random.shuffle(values)
    while values:
        yield values.pop()
    raise StopIteration
def display_indicator(indicator_list):
    x = 200
    if not indicator_list == {}:
        pygame.draw.rect(screen, (208,208,208), Rect(325,275,200,15))
    indicator_list_local = {}
    for a,b in zip(range(4),randrange(0, 4)):
        indicator_list_local[a] = indicator_list.get(b)
    for a in indicator_list_local.values():
        if a == 2:
            pygame.draw.ellipse(screen,(255,255,255),(x+25,275,15,15))
        if a == 1:
            pygame.draw.ellipse(screen,(1,1,1),(x+25,275,15,15))
        x += 20
def highlight_indicator_list(guess):
    indicator_list = {}
    master_list_local = master_list.copy()
    for eachVal, a, i in zip(guess, master_list_local, range(4)):
        if eachVal == master_list_local[a]:
            indicator_list[i] = 1
            master_list_local.pop(i)
            guess.pop(guess.index(eachVal))
    masterList = []
    for v in master_list_local.values():
        masterList.append(v)
    while guess != {}:
        #check if each value remaining in guess is in master
        i = 0
        remaining = guess.pop()
        if remaining in masterList:
            while 1:
                if indicator_list.has_key(i) == False:
                    indicator_list[i] = 2
                    masterList.remove(remaining)
                    i += 1
                    break
                else:
                    i += 1
        if len(guess) == 0:
            break
    display_indicator(indicator_list)

def compare(all_attempts_list,master_list, attempt):
    global attempts
    guess = []
    master = []
    for eachVal, a in zip(attempt_map[attempt], range(4)):
        guess.append(all_attempts_list[eachVal])
        master.append(master_list[a])
    if guess == master:
        return True
    else:
        highlight_indicator_list(guess)
        attempts.append(1)
        return False

init_elli()
gen_colors()
gen_master()
draw_palette()
draw_elli(None,None,None)
init_attempt_map()
gobut = Button(165,375,"check.gif")
# put the button on the screen
screen.blit(gobut.image,gobut.rect)
my_font = pygame.font.SysFont("arial", 12)
#background = pygame.image.load(logo_image_filename).convert()
mastmind_text = my_font.render("pyMastermind", True, (255,255,255), (0, 0, 0))
screen.blit(mastmind_text, (20,20))
while True:

    for event in pygame.event.get():

        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            check_color_selection(pygame.mouse.get_pos())
            for a in range(len(BOARD)):
                if BOARD[a].collidepoint(pygame.mouse.get_pos()):
                    try:
                        draw_elli(attempts_list,a,all_attempts_list)
                    except:
                        pass
            if gobut.clicked(pygame.mouse.get_pos()):  #check if the button's limits are clicked
                gobut.press()  #depress the button
                screen.blit(gobut.image,gobut.rect)  #update the screen
                if len(all_attempts_list) % 4 == 0 and len(all_attempts_list) > 3:
                    if (len(all_attempts_list) /4  - 1) == len(attempts):
                        win = compare(all_attempts_list,master_list,(len(all_attempts_list) / 4)-1)
                    if not win and len(attempts) > 9:
                        print_master()
                        text_surface = my_font.render("No Victory", True, (0,0,0), (255, 255, 255))
                        screen.blit(text_surface, (45, 75))
                    elif win:
                        print_master()
                        text_surface = my_font.render("VICTORY!!!", True, (0,0,0), (255, 255, 255))
                        screen.blit(text_surface, (35, 75))
                pygame.draw.rect(screen, (208,208,208), Rect(235,250,15,15))
                text_surface_guess = my_font.render("Current Guess:", True, (0,0,0), (255, 255, 255))
                screen.blit(text_surface_guess, (155, 275))
                pygame.display.flip()  #update display


            pygame.draw.rect(screen, (0,0,0), Rect(235,250,15,15))
            if color_select <> []:
                pygame.draw.ellipse(screen,code_list[color_select],(235,250,15,15))
            text_surface = my_font.render("Color Selected:", True, (0,0,0), (255, 255, 255))
            screen.blit(text_surface, (155, 250))
        screen.blit(mastmind_text, (20,20))
        screen.blit(gobut.image,gobut.rect)
        gobut.popup()
        pygame.display.update()
