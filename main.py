from pygame import *
import os
from threading import *
import levels
import hud
import tiger
init()

on = True # Set this to false to end the game
screen = display.set_mode((100,100)) # this size will be set in gamewindow creation
first = True # for functions that need first time setup
toblit = [0,0,0,0]
keax,keay = 0,0
inair = 50
levelbackground = 0
mode = "collection"
itemstoblit = []
stage = 0
shiftpressed = False
attack = "peck"

class Physics:
    def __init__(self):
        self.grav_inc = 0
    def gravity(self, acc=9.8):
        self.grav_inc = 1
        return self.grav_inc
    def cleargrav(self):
        self.grav_inc = 0
phy = Physics()

def itemsrender():
    global itemstoblit
    tmp = levels.collection()
    if tmp != "none":
        for i in range(0, len(itemstoblit)):
            try:
                if tmp[2] == itemstoblit[i][2]:
                    if tmp[3] == "delete":
                        itemstoblit.pop(i)
                    itemstoblit[i] = tmp
                    tmp = 0
            except: pass
        if tmp != 0: itemstoblit.append(tmp)

class Gamewindow:
    global on, screen, first, levelbackground, itemstoblit, keax, keay
    def __init__(self, size):
        global levelbackground, keax, keay
        levels.size = size
        self.tmp = levels.supermarket()
        """supermarket()"""
        toblit[0] = (self.tmp[0],(0,0))
        keax = self.tmp[1][0]
        keay = self.tmp[1][1]
        '''for i in range(0, len(self.tmp[1])):
            toblit.append(self.tmp[1][i])'''
        print toblit
        #screen = display.set_mode(size)
        self.mainfunc = []
        self.tm = time.Clock()
    def changelevel(self, level_function):
        global itemstoblit, keax, keay
        # cleanup
        levels.collectionitems = []
        itemstoblit = []
        levels.platformvalues = []
        self.mainfunc = []
        levels.changelevels = 0
        # start new level
        self.tmp = level_function()
        keax = self.tmp[1][0]
        keay = self.tmp[1][1]
        toblit[0] = (self.tmp[0],(0,0))
        self.addtomain(kea)
        self.addtomain(hud.renderenergy)
        self.addtomain(itemsrender)
        self.addtomain(levels.addtomain)
        self.addtomain(animalrender)
        self.addtomain(itemsrender)
    def addtomain(self, function):
        self.mainfunc.append(function)
    def mainloop(self):
        global on, first
        while on:
            self.tm.tick(400)
            for e in event.get():
                if e.type == QUIT:
                    on = False
                if e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        on = False
            for i in range(0, len(self.mainfunc)):
                self.mainfunc[i]()
            # Check for level change
            if levels.changelevels != 0:
                self.changelevel(levels.changelevels)
flying = False

keadir = "left"

def controls():
    global inair, flying, attack, keadir
    keys = key.get_pressed()
    click = mouse.get_pressed()
    xinc = 0
    yinc = 0
    dir = 'unknown'
    if keys[K_w]:
        if hud.energy > 0:
            if click[2]:
                flying = True
                yinc = -1
                hud.energy -=1
            elif inair < 50:
                flying = False
                inair +=0.001
                yinc = (inair-50)/20
                hud.energy -=0.5
        else: flying = False
    else: flying = False
    if tiger.keabackforthmove == False:
        if keys[K_a]:
            dir = "left"
            if hud.energy > 0:
                xinc = -1
                hud.energy -=0.05
            else:
                xinc = -0.1
        if keys[K_d]:
            dir = 'right'
            if hud.energy > 0:
                xinc = 1
                hud.energy -=0.05
            else:
                xinc = 0.1
    else:
        if keadir == "left":
            xinc = -1
        else:
            xinc = 1
        if keax < 1:
            keadir = "right"
            dir = "right"
        if keax > 1920/2-43:
            keadir = "left"
            dir = "left"
    if levels.mode == "fight":
        if click[0]:
            # TODO: attack animations here
            tiger.sendattack(attack)
    if keys[K_1]:
        attack = "peck"
    if keys[K_2]:
        attack = 'grab'
    if keys[K_3]:
        attack = "laserbeam"
    return xinc, yinc, dir

def blitquque(img, (x,y)): # this is so multithread bliting can occur, instead of bliting, call this func /w same para
    global toblit
    tmp = (img,(x,y))
    toblit.append(tmp)

def platforms(x,y): # (platform_x1, platform_y1, platform_x2, platform_y2) All platforms are square.
    for i in range(0, len(levels.platformvalues)):
        if not ((y + 32 < levels.platformvalues[i][1]) or  (y > levels.platformvalues[i][3])): # inside y range
            if not ((x < levels.platformvalues[i][0]) or  (x +32 > levels.platformvalues[i][2])): # inside x range
                # on platform
                return False
    return True

class Graphics:
    keagf = os.path.join("assets", "kea.png")
    keaim = image.load(keagf).convert_alpha()
    keaimg = keaim
    keaimf = image.load(os.path.join("assets", "keaflight.png")).convert_alpha()
    barframe = image.load(os.path.join("assets", "energybarframe.png")).convert_alpha()
    #blackimg = image.load(os.path.join("assets", "black.png")).convert_alpha()

inaircoolcount = 0

def kea():
    global first, keax,keay, inair, inaircoolcount, flying
    if tiger.changekeapos != 0:
        keax, keay = tiger.changekeapos[0], tiger.changekeapos[1]
        tiger.changekeapos = 0
    xinc,yinc,dir = controls()[0], controls()[1], controls()[2]
    toblit[1] = (Graphics.keaimg, (keax,keay))
    if flying:
        if dir == "right":
            Graphics.keaimg = Graphics.keaimf
        elif dir == 'left':
            Graphics.keaimg = transform.flip(Graphics.keaimf, True, False)
    else:
        if dir == "right":
            Graphics.keaimg = Graphics.keaim
        elif dir == 'left':
            Graphics.keaimg = transform.flip(Graphics.keaim, True, False)
    keax +=xinc
    keay +=yinc
    #so can't go off screen
    # TODO if have time: scrolling
    if keax < 0:
        keax =0
    if keax > 1920/2-42:
        keax = 1920/2-42
    # gravity and ground stuff
    if not flying:
        if platforms(keax, keay):
            keay += phy.gravity()
            if inair < 50:
                inair +=1
        else:
            # jump cool down time
            if inaircoolcount > 100:
                inair =0
                inaircoolcount = 0
            else:
                inaircoolcount +=1
    levels.keax, levels.keay = keax, keay


#multi-threading

#Rendering thread
class Render(Thread):
    global on, toblit, screen, teststone
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global toblit, screen, shiftpressed, teststone
        display.set_mode((1920/2,1080/2))
        while on:
            toblit[2] = hud.toblit # fixme
            for i in range(0, len(toblit)):
                if toblit[i] != 0:
                    try:
                        screen.blit(toblit[i][0], toblit[i][1])
                    except: pass
            for i in range(0, len(itemstoblit)):
                try:
                    screen.blit(itemstoblit[i][0], itemstoblit[i][1])
                except:
                    pass
            if not levels.clutterfree:
                if tiger.stonerender != 0:
                    screen.blit(tiger.stonerender[0], (tiger.stonerender[1], tiger.stonerender[2]))
                screen.blit(Graphics.barframe, (0,0))
                if tiger.tigerhealthrender != 0:
                    if levels.mode == "fight":
                        screen.blit(tiger.tigerhealthrender, (27, 40))
                if levels.mode == "fight": screen.blit(Graphics.barframe, (0,40))
                if hud.text_img != 0:
                    screen.blit(hud.text_img, (0,0))
                if hud.timerrender !=0:
                    screen.blit(hud.timerrender, levels.timerpos)
            if levels.keachain !=0:
                screen.blit(levels.keachain, (levels.endchainkea[0], levels.endchainkea[1]))
            display.flip()

def animalrender():
    toblit[3] = levels.animalblit


# Unused
def checkaddtomain():
    if levels.addtomain != 0:
        g.addtomain(levels.addtomain)
        print "added"
    levels.addtomain = 0

#everything else
class Main(Thread):
    global on, toblit
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        global g
        g = Gamewindow((1920/2,1080/2))
        g.addtomain(kea)
        g.addtomain(itemsrender)
        g.addtomain(animalrender)
        g.addtomain(levels.addtomain)
        g.addtomain(hud.renderenergy)
        g.mainloop()

Render()
Main()
while on:
    pass

