from pygame import image, transform
import os
import random
import levels
import hud
import sound

tigeraniindex = -1
tigerframetracker = 0
attack = 0 # Always reset to 0 after attack has been dealt with.
attacktimeout = 0

health = 0

tigerhealthrender = 0

changekeapos = 0

stonerender = 0

keabackforthmove = False

def sendattack(attack_):
    global attack
    attack = attack_
class Tiger:
    global tigeraniindex, health, tigerframetracker, tigerhealthrender, stonehittimeout, attack, stonex, stoney, attacktimeout, tigerhealthrender, changekeapos, stonerender
    def __init__(self):
        self.animation = [
            image.load(os.path.join("assets", "tiger", "tiger.png")).convert_alpha(),
            image.load(os.path.join("assets", "tiger", "tiger2.png")).convert_alpha(),
            image.load(os.path.join("assets", "tiger", "tiger3.png")).convert_alpha(),
            image.load(os.path.join("assets", "tiger", "tiger4.png")).convert_alpha(),
            image.load(os.path.join("assets", "tiger", "tiger5.png")).convert_alpha(),
            image.load(os.path.join("assets", "tiger", "tiger6.png")).convert_alpha(),
            image.load(os.path.join("assets", "tiger", "tiger7.png")).convert_alpha(),
            image.load(os.path.join("assets", "tiger", "tiger8.png")).convert_alpha(),
            image.load(os.path.join("assets", "tiger", "tiger9.png")).convert_alpha(),
            image.load(os.path.join("assets", "tiger", "tiger10.png")).convert_alpha(),
            image.load(os.path.join("assets", "tiger", "tiger11.png")).convert_alpha(),
            image.load(os.path.join("assets", "tiger", "tiger12.png")).convert_alpha()
        ]
        self.mdir = "mr" # Move, direction. eg ml = move left, left just means face left without animation.
        self.x = 0
        self.y = 346
        self.yinc = 0
        self.health = 10
        self.stone = Stone()
    def render(self):
        global tigeraniindex,tigerframetracker, stonerender
        stonerender = self.stone.render()
        tigerframetracker +=1
        if tigeraniindex > len(self.animation)-2:
            tigeraniindex = -1
        if tigerframetracker % 21 == 0:
            tigeraniindex += 1
        if tigerframetracker > 500: tigerframetracker = 0
        if self.mdir == "ml":
            return self.animation[tigeraniindex]
        elif self.mdir == "mr":
            return transform.flip(self.animation[tigeraniindex], True, False)
        elif self.mdir == "l":
            return self.animation[0]
        elif self.mdir == "r":
            return transform.flip(self.animation[0], True, False)
    def collisions(self):
        global attack, attacktimeout, changekeapos
        if self.mdir == "mr":
            if self.x+150 < levels.keax < self.x + 200:
                if self.y < levels.keay < self.y + 100:
                    self.__init__()
                    changekeapos = (200,100)
                    hud.energy = hud.energysave[0]
        if self.mdir == "ml":
            if self.x < levels.keax < self.x + 50:
                if self.y < levels.keay < self.y + 100:
                    self.__init__()
                    changekeapos = (200,100)
                    hud.energy = hud.energysave[0]
        if attacktimeout <= 0:
            if self.x < levels.keax < self.x + 200:
                if self.y < levels.keay < self.y + 100:
                    if attack != 0:
                        if attack == "peck":
                            # TODO: animate
                            self.health -=1
                            attack = 0
                            sound.tigergrowl()
                        elif attack == "grab":
                            #print "grabing is not yet implemented, and a tiger is far too big anyway what are you thinking? I mean this is way more unrealistic than laser beam shooting keas!"
                            attack = 0
                        elif attack == 'laserbeams':
                            #print "Laser beams are no yet implemented."
                            attack = 0
                        attacktimeout = 500
        else:
            attacktimeout -=1
    def jump(self, mode):
        if mode == "up":
            self.yinc = -2
            self.y = 346
        else:
            if self.yinc > -0.1:
                self.yinc = 2
    def checkdead(self):
        global stonex, stoney, stonehittimeout, tigerhealthrender, stonerender
        # if intersects with rock
        if stonehittimeout > 200:
            if self.x < stonex < self.x + 200:
                if self.y < stoney < self.y + 50:
                    self.health -=4
                    stonehittimeout = 0
                    sound.tigergrowl()
        else:
            stonehittimeout +=1
        if self.health <= 0:
            if self.y < 1000:
                self.y +=2
            else:
                levels.changelevels = levels.carpark
                self.health = 10
                tigerhealthrender = 0
                stonerender = 0
    def ai(self):
        global health, tigerhealthrender
        self.checkdead()
        if levels.mode == "fight":
            tigerhealthrender = hud.rendertigerhealth(self.health)
        else: tigerhealthrender = 0
        health = self.health
        # move is preset direction
        self.collisions()
        self.y += self.yinc
        self.yinc = self.yinc*0.99
        if self.y >= 346:
            self.yinc = 0
            if random.randint(0, 2000) == 1:
                self.jump("up")
        else:
            if 516 < self.x < 847:
                self.jump("down")
        if self.mdir == "ml":
            self.x -=(self.health*0.1) # speed is proportional to health
        if self.mdir == "mr":
            self.x +=(self.health*0.1)
        if self.x < 0:
            self.mdir = "mr"
        if self.x > 1920/2-250:
            self.mdir = "ml"
        return (self.x,self.y)

stonex=0
stoney=0
stonehittimeout=0

class Stone:
    global stonex, stoney, attacktimeout
    def __init__(self,sx=0, sy=0):
        global attacktimeout, attack
        self.img = image.load(os.path.join("assets", "stone.png")).convert_alpha()
        self.keafriend = image.load(os.path.join("assets", "keacarrystone.png")).convert_alpha()
        self.x = sx
        self.y = sy
        self.grabed = False
        self.initial = True
        self.deliverymode = False
    def frienddelivery(self):
        #self.x = -50
        #self.y = 200
        if tigerframetracker % 21:
            self.x +=0.5
            self.y -=2.5
            if self.y < 0:
                self.deliverymode = False
    def render(self):
        global attacktimeout, attack, stonex, stoney
        if attacktimeout <= 0:
            if self.x-32 < levels.keax < self.x + 32:
                if self.y-32 < levels.keay < self.y + 32:
                    if attack != 0:
                        if attack == "grab":
                            if self.grabed:
                                self.grabed = False
                                attack = 0
                            else:
                                self.grabed = True
                                self.initial = False
                                attack = 0
                        attacktimeout = 500
        if self.grabed:
            self.x = levels.keax
            self.y = levels.keay + 20
        else:
            if self.y < 230:
                self.y +=1
            if self.initial == False:
                if not self.y > 1000:
                    self.y +=1
        stonex = self.x
        stoney = self.y
        if self.y > 1000:
            if random.randint(0, 1000) == 1:
                self.x = -50
                self.y = 200
                self.deliverymode = True
                self.initial = True
        if self.deliverymode:
            self.frienddelivery()
        if self.deliverymode: return self.keafriend, self.x, self.y
        else: return self.img, self.x, self.y

class Turkey:
    global tigeraniindex, health, tigerframetracker, stonehittimeout, attack, stonex, stoney, attacktimeout, tigerhealthrender, changekeapos, stonerender, keabackforthmove
    def __init__(self):
        self.robo0 = image.load(os.path.join("assets", "turkey", "turkey_normal.png")).convert_alpha()
        self.robo1 = image.load(os.path.join("assets", "turkey", "turkey_robo2.png")).convert_alpha()
        self.robo2 = image.load(os.path.join("assets", "turkey", "turkey_robo3.png")).convert_alpha()
        self.robo3 = image.load(os.path.join("assets", "turkey", "turkey_robo4.png")).convert_alpha()
        self.robo4 = image.load(os.path.join("assets", "turkey", "turkey_robo5.png")).convert_alpha()
        self.mdir = "mr" # Move, direction. eg ml = move left, left just means face left without animation.
        self.x = 0
        self.y = 400
        self.yinc = 0
        self.health = 10
        self.stone = Stone()
        self.littleturkey = 0
        self.robo = 0
        self.spawncount = 0
    def render(self):
        if self.robo == 0:
            if self.mdir == "mr": return self.robo0
            else: return transform.flip(self.robo0, True, False)
        elif self.robo == 1:
            if self.mdir == "mr": return self.robo1
            else: return transform.flip(self.robo1, True, False)
        elif self.robo == 2:
            if self.mdir == "mr": return self.robo2
            else: return transform.flip(self.robo2, True, False)
        elif self.robo == 3:
            if self.mdir == "mr": return self.robo3
            else: return transform.flip(self.robo3, True, False)
        elif self.robo >= 4:
            if self.mdir == "mr": return self.robo4
            else: return transform.flip(self.robo4, True, False)
    def collisions(self):
        global attack, attacktimeout, changekeapos, keabackforthmove
        if attacktimeout <= 0:
            if self.x < levels.keax < self.x + 130:
                if self.y < levels.keay < self.y + 100:
                    if attack != 0:
                        if attack == "peck":
                            # TODO: animate
                            self.robo +=1
                            print self.robo
                            if self.robo == 4:
                                keabackforthmove = True
                            attack = 0
                        elif attack == "grab":
                            #print "grabing is not yet implemented, and a tiger is far too big anyway what are you thinking? I mean this is way more unrealistic than laser beam shooting keas!"
                            attack = 0
                        elif attack == 'laserbeams':
                            #print "Laser beams are no yet implemented."
                            attack = 0
                        attacktimeout = 500
        else:
            attacktimeout -=1
    def jump(self, mode):
        if mode == "up":
            self.yinc = -2
            self.y = 399
            self.littleturkey = Tinyturkeys(self.robo4, self.x, self.y)
        else:
            if self.yinc > -0.1:
                self.yinc = 2
    def checkdead(self):
        global stonex, stoney, stonehittimeout
        # if intersects with rock
        if stonehittimeout > 200:
            if self.x < stonex < self.x + 200:
                if self.y < stoney < self.y + 50:
                    self.health -=2
                    stonehittimeout = 0
        else:
            stonehittimeout +=1
        if self.health <= 0:
            if self.y < 1000:
                self.y +=2
            else:
                levels.changelevels = levels.endchain
                self.health = 10
    def ai(self):
        self.spawncount +=1
        global health, tigerhealthrender, stonerender
        self.checkdead()
        tigerhealthrender = hud.rendertigerhealth(self.health)
        health = self.health
        # move is preset direction
        if self.robo >= 4:
            if self.littleturkey !=0:
                stonerender = self.littleturkey.render()
                if self.littleturkey.x > 1000 or self.littleturkey.x < -80:
                    self.littleturkey = 0
            else:
                if self.spawncount >= 100:
                    self.littleturkey = Tinyturkeys(self.robo4, self.x, self.y)
                    self.health -=0.4
                    self.spawncount = 0
        self.collisions()
        self.y += self.yinc
        self.yinc = self.yinc*0.99
        if self.y >= 399:
            self.yinc = 0
            if random.randint(0, 2000) == 1:
                self.jump("up")
        else:
            self.jump("down")
        if self.mdir == "ml":
            self.x -=(self.health*0.1) # speed is proportional to health
        if self.mdir == "mr":
            self.x +=(self.health*0.1)
        if self.x < 0:
            self.mdir = "mr"
        if self.x > 1920/2-250:
            self.mdir = "ml"
        return (self.x,self.y)

class Tinyturkeys:
    global changekeapos
    def __init__(self, images, startx, starty):
        self.img = transform.scale(images, (130/3,100/3))
        self.dir = random.randint(0,1)
        self.x, self.y = startx, starty
        if self.dir == 0:
            pass
        else:
            self.img = transform.flip(self.img, True, False)
        self.y = 430
    def collisions(self):
        global changekeapos
        if self.x < levels.keax < self.x + 32:
            if self.y-20 < levels.keay+20 < self.y + 32:
                changekeapos = (200,100)
                hud.energy = hud.energysave[0]
    def render(self):
        self.collisions()
        if self.dir == 0:
            self.x +=1.6
        else:
            self.x -=1.6
        return self.img, self.x, self.y