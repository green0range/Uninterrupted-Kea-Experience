from pygame import *
import os
import time
import food
from tiger import Tiger, Turkey
import hud
import sound
size = (0,0)

platformvalues = []

mode = "collection"
keax, keay = 0, 0
collectionitems = []
animalblit = 0

changelevels = 0

addtomain = 0

animal = ""

timerpos = (0,0)

i = 0

def collection():
    global i
    if mode == "collection":
        reach = 150
        mousex, mousey = mouse.get_pos()
        if i < (len(collectionitems)-1):
            if keax-reach < mousex < keax+reach:
                if keay-reach < mousey < keay+reach:
                    if not ((collectionitems[i+1][1][1] + 32 < mousey) or  (collectionitems[i+1][1][1] > mousey)): # inside y range
                        if not ((collectionitems[i+1][1][0] + 32 < mousex) or  (collectionitems[i+1][1][0] > mousex)): # inside x range
                            i +=1
                            if mouse.get_pressed()[0]:
                                if collectionitems[i][2]:
                                    hud.energy += 500*collectionitems[i][3]
                                else: hud.energy -= 500*collectionitems[i][3]
                                collectionitems.pop(i)
                                return 0, 0, i, "delete"
                            return collectionitems[i][0].render(True), collectionitems[i][1], i, "keep"
            # will not be reached if first return true
            i +=1
            return collectionitems[i][0].render(False), collectionitems[i][1], i, "keep"
        else: i =0
    return "none"

timeri = 0
timers = 0
def timer():
    global timers, timeri, changelevels
    timeri += 1
    if timeri >= 400:
        timeri = 0
        timers += 1
        hud.timer()
    if timers == 20:
        if animal == "tiger":
            changelevels = tiger
        elif animal == "turkey":
            changelevels = turkey
        hud.energysave[0] = hud.energy
        hud.timerrender = 0


def supermarket():
    global size, platformvalues, addtomain, timerpos, animal
    time.sleep(0.1) # on some systems this happens faster than the display can be created, causing a "No video mode has been set" error
    addtomain = timer
    hud.con = "bk"
    animal = "tiger" # level name of following fight
    timerpos = (1920/2-60,1080/2-60)
    bg = image.load(os.path.join("assets", "levels", "supermarket.png")).convert()
    platforms = [
        (0,460,960,470),

        (0,400,115,410),
        (0,350,115,360),
        (0,300,115,310),
        (0,230,115,240),
        (0,175,115,185),

        (210,180,420,190),
        (210,240,420,250),
        (210,245,420,255),
        (210,351,420,361),
        (210,400,420,410),

        (570,180,780,190),
        (570,240,780,250),
        (570,245,780,255),
        (570,351,780,361),
        (570,400,780,410),

        (850,400,960,410),
        (850,350,960,360),
        (850,300,960,310),
        (850,230,960,240),
        (850,175,960,185)
    ]
    for i in range(0, len(platforms)):
        platformvalues.append(platforms[i])
    fooditems = [
        food.Banana(),
        food.Apple(),
        food.Cookie(),
        food.Pie(),
        food.Windscreenwiper()
    ]

    collectionitems.append((fooditems[0], (0,0), True, 1)) # Phantom banana
    collectionitems.append((fooditems[2], (56,150), False, 1))
    collectionitems.append((fooditems[1], (178,484), True, 1))
    collectionitems.append((fooditems[0], (307,280), True, 1))
    collectionitems.append((fooditems[3], (492,423), False, 1))
    collectionitems.append((fooditems[0], (400,500), True, 1))
    collectionitems.append((fooditems[2], (450,639), False, 1))
    collectionitems.append((fooditems[0], (356,760), True, 1))
    collectionitems.append((fooditems[0], (674,160), True, 1))

    collectionitems.append((fooditems[1], (288,484), True, 1))
    collectionitems.append((fooditems[0], (417,280), True, 1))
    collectionitems.append((fooditems[3], (602,423), False, 1))
    collectionitems.append((fooditems[0], (510,500), True, 1))
    collectionitems.append((fooditems[2], (560,639), False, 1))
    collectionitems.append((fooditems[0], (266,760), True, 1))
    collectionitems.append((fooditems[0], (584,160), True, 1))

    collectionitems.append((fooditems[1], (886,182), True, 1))
    collectionitems.append((fooditems[0], (907,340), True, 1))
    collectionitems.append((fooditems[3], (586,300), False, 1))
    collectionitems.append((fooditems[0], (577,229), True, 1))
    collectionitems.append((fooditems[2], (482,487), False, 1))
    collectionitems.append((fooditems[0], (707,393), True, 1))
    collectionitems.append((fooditems[0], (719,500), True, 1))

    collectionitems.append((fooditems[1], (786,182), True, 1))
    collectionitems.append((fooditems[0], (807,340), True, 1))
    collectionitems.append((fooditems[3], (516,300), False, 1))
    collectionitems.append((fooditems[0], (677,229), True, 1))
    collectionitems.append((fooditems[2], (282,487), False, 1))
    collectionitems.append((fooditems[0], (607,393), True, 1))
    collectionitems.append((fooditems[0], (819,500), True, 1))

    hud.text("|||||So you're really going through with this?-|I have to do this. They're going to attack the kea village.-|That doesn't matter! I can take them all!-|Don't be an idiot. Whiskers would tear you apart.-|But what makes you think that you have a better|chance than me?-|...-|You don't even have a plan, do you.-|Yes I do!-|What's that?-|Peck it a bit, then kill it 'til it dies!-|...-|Well, I'll be on my way now...-|Wait! I'll help you. I can bring rocks to you|for you to drop on him.-|I guess that would help. Thanks, Blue.-|Good luck, YellowBeak.", img1=image.load(os.path.join("assets", "story", "kea.png")).convert(), img=image.load(os.path.join("assets", "story", "bluekea.png")).convert(), imgco=(20,20))
    sound.collect1()
    return (bg, (0,0))

def tiger():
    global size, platformvalues, addtomain, mode, animal
    mode = "fight"
    animal = "tiger"
    hud.con = "ti"
    tiger.tigerhealthrender = 0
    time.sleep(0.1) # on some systems this happens faster than the display can be created, causing a "No video mode has been set" error
    bg = image.load(os.path.join("assets", "levels", "tiger.png")).convert()
    platforms = [
        (0,442,1596,452),

        (50,74,284,84),
        (182,76,752,86),
        (864,80,1076,90),
        (1162,1558,755,90),

        (0,270,616,280),
        (844,270,1360,280),
        (1550,270,1596,280),
    ]
    for i in range(0, len(platforms)):
        platformvalues.append(platforms[i])
    global ti
    ti = Tiger()
    addtomain = runtiger

    hud.text("||||Welcome, kea, to my domain.-|It just looks like a broken concrete warehouse to me.-|Such hostility! What has brought you here, dear|kea, to this place and state of mind?-|I know what you intend, Whiskers. The annihalition of all others.|Complete dominance over the kingdom, attainable only through|a genocide absolute.-|Such long, angry words. Your syllables have malice|in them, and your intent is clear. You are here|to fight, are you not?-|I will destroy you.-|Well. If you want to start a battle that you have|no chance of winning, then who am I to refuse|you? En Guarde!", img=image.load(os.path.join("assets", "story", "tiger.png")).convert(), img1=image.load(os.path.join("assets", "story", "kea.png")).convert(), imgco=(20,20))
    sound.tigerbattle()
    return (bg, (200,100))

def turkey():
    global size, animal, platformvalues, addtomain, mode, changelevels
    mode = "fight"
    animal = "turkey"
    hud.con = "tu"
    bg = image.load(os.path.join("assets", "levels", "turkey.png")).convert()
    platforms = [
        (0,460,960,470),

        (82,80,258,90),
        (178,251,329,261),
        (428,146,578,156),
        (605,320,755,330),
    ]
    for i in range(0, len(platforms)):
        platformvalues.append(platforms[i])

    global tu
    tu = Turkey()
    addtomain = runtiger

    hud.text("|||||I don't recognise this place. I must have taken|a wrong turn.-|HELLO KEA-|... Hello?-|welcome to turkey-|Um. Thanks, I guess?-|oim a turkee-|Oh. I never would have guessed.-|you wann fit brah-|What?-|or ar ya too chiken?-|... Is that some sort of joke?-|You're a joke.-|Even so, you are a turkey. Do you really want|to fight?-|I think that your time is up, YellowBeak.-|I don't think anything could be further from the|truth. Let's go, turkey.-|Or are you too chicken?-|(his gobbles are indecipherable)", img=image.load(os.path.join("assets", "story", "kea.png")).convert(), img1=image.load(os.path.join("assets", "story", "turkey.png")).convert(), imgco=(20,20))
    sound.turkeybattle()
    return (bg, (200,100))

def carpark():
    global size, platformvalues, addtomain, timerpos, mode, timers, timeri, animal
    mode = "collection"
    animal = "turkey"
    time.sleep(0.1) # on some systems this happens faster than the display can be created, causing a "No video mode has been set" error
    sound.collect1()
    timeri = 0
    timers = 0
    addtomain = timer
    timerpos = (10, 40)
    bg = image.load(os.path.join("assets", "levels", "carpark.png")).convert()
    platforms = [
        (0,500,960,510),

        (40,427,86,437),
        (102,395,191,405),
        (757,422,816,432),
        (830,395,918,405),
        (393,491,461,501)
    ]
    for i in range(0, len(platforms)):
        platformvalues.append(platforms[i])
    fooditems = [
        food.Banana(),
        food.Apple(),
        food.Cookie(),
        food.Pie(),
        food.Windscreenwiper()
    ]

    collectionitems.append((fooditems[0], (0,0), True, 1)) # Phantom banana
    collectionitems.append((fooditems[2], (56,484), False, 1))
    collectionitems.append((fooditems[1], (178,494), True, 1))
    collectionitems.append((fooditems[0], (307,484), True, 1))
    collectionitems.append((fooditems[3], (492,483), False, 1))
    collectionitems.append((fooditems[0], (400,500), True, 1))
    collectionitems.append((fooditems[2], (450,639), False, 1))
    collectionitems.append((fooditems[0], (356,760), True, 1))
    collectionitems.append((fooditems[0], (674,484), True, 1))

    collectionitems.append((fooditems[1], (288,487), True, 1))
    collectionitems.append((fooditems[0], (417,484), True, 1))
    collectionitems.append((fooditems[3], (602,423), False, 1))
    collectionitems.append((fooditems[0], (510,500), True, 1))
    collectionitems.append((fooditems[2], (560,639), False, 1))
    collectionitems.append((fooditems[0], (266,760), True, 1))
    collectionitems.append((fooditems[0], (584,584), True, 1))

    collectionitems.append((fooditems[1], (886,484), True, 1))
    collectionitems.append((fooditems[0], (907,440), True, 1))
    collectionitems.append((fooditems[3], (586,500), False, 1))
    collectionitems.append((fooditems[0], (577,464), True, 1))
    collectionitems.append((fooditems[2], (482,487), False, 1))
    collectionitems.append((fooditems[0], (707,484), True, 1))
    collectionitems.append((fooditems[0], (719,500), True, 1))

    collectionitems.append((fooditems[1], (786,484), True, 1))
    collectionitems.append((fooditems[0], (807,340), True, 1))
    collectionitems.append((fooditems[3], (516,300), False, 1))
    collectionitems.append((fooditems[0], (677,404), True, 1))
    collectionitems.append((fooditems[2], (282,487), False, 1))
    collectionitems.append((fooditems[0], (607,444), True, 1))
    collectionitems.append((fooditems[0], (819,500), True, 1))

    collectionitems.append((fooditems[1], (605,63), True, 1))
    collectionitems.append((fooditems[1], (615,73), True, 1))
    collectionitems.append((fooditems[1], (690,63), False, 1))
    collectionitems.append((fooditems[1], (700,103), True, 1))
    collectionitems.append((fooditems[1], (605,200), False, 1))
    collectionitems.append((fooditems[1], (690,173), True, 1))
    collectionitems.append((fooditems[1], (615,242), True, 1))

    collectionitems.append((fooditems[4], (73-16,425-16), True, 5))
    collectionitems.append((fooditems[4], (801-14,421-14), True, 5))

    #hud.text("Arh, we're moving up in the world. But, more energy is needed, apprently, car windscreen wipers are great food!", img=image.load(os.path.join("assets", "story", "kea.png")).convert(), imgco=(20,20))
    sound.collect2()
    return (bg, (0,0))

endchainkea = [701,104]

clutterfree = False

def endchain():
    global addtomain, keachain, clutterfree
    baseimg = image.load(os.path.join("assets", "endgame", "foodchain.png")).convert()
    kea = image.load(os.path.join("assets", "endgame", "kea.png")).convert()
    keachain = kea
    clutterfree = True

    addtomain = keamovetotop

    return (baseimg, (-1000,1000))

keachain = 0

def keamovetotop():
    if endchainkea[0] > 60:
        endchainkea[0] -=1
    if endchainkea[1] < 270:
        endchainkea[1] +=1


def runtiger():
    global animalblit, ti, animal, tu
    if animal =="tiger":
        animalblit = (ti.render(), ti.ai())
    if animal == "turkey":
        animalblit = (tu.render(), tu.ai())