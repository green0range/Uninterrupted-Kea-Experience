from pygame import font, Surface, image
from time import sleep
import tiger
import os
import levels
import sound

energy = 3000
toblit = 0
toblit2 = 0
font.init()
hudfont = font.Font(os.path.join("assets", "fonts", "VT323-Regular.ttf"), 20)
hudfonttimer = font.Font(os.path.join("assets", "fonts", "VT323-Regular.ttf"), 40)
s = Surface((1813/2, 30))
s.set_colorkey((0,255,0))
st = Surface((1920/2, 1080/2))
st.fill((255,255,255))
sh = Surface((1813/2, 30))
sh.set_colorkey((0,255,0))
timerrender = 0
energysave = [100000] # tiger fight,


text_img = 0 # picked up by render thread if not 0

def rendertigerhealth(h):
    global energy, toblit2, s
    tigerhealthpercent = tiger.health*10.0
    sh.fill((0,255,0))
    sh.fill((235,145,20), rect=((1920/2-((tigerhealthpercent/100)*1920/2),0,1920/2, 30)))
    sh.blit(hudfont.render(levels.animal + " health: " + str(tigerhealthpercent) + "%", 0, (100,100,100)),(10,3))
    return sh


def renderenergy():
    global energy, toblit, s
    energypercent = energy/100
    s.fill((0,255,0))
    if energy < 0: energy = 0
    if energy > 10000:
        energy = 10000
    try: # Invalid colour if energy goes negative.
        s.fill((200,200*(energypercent/100),200*(energypercent/100)),((1920/2-((energypercent/100)*1920/2),0,1920/2, 30)))
    except TypeError:
        s.fill((200,0,0),((1920/2-((energypercent/100)*1920/2),0,1920/2, 30)))
    s.blit(hudfont.render("Energy: " + str(round(energypercent, 3)) + "%", 0, (100,100,100)),(10,3))
    toblit = (s,(27,0))

con = "bk"

def text(txt, img=0, imgco=(200, 400), img1=0):
    global text_img, st
    t = list(txt)
    td = ["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]
    row = 0
    textstart = 5
    if con == "bk":
        sound.bluesquawk()
    elif con == "ti":
        sound.tiger()
    elif con == "tu":
        sound.keasquawk()
    for i in range(0, len(t)):
        q = i
        if t[i] == "|":
            t[i] = ""
            row +=1
        td[row] += t[i]
    if img != 0:
        st.blit(img, imgco)
    if img != 0:
        st.blit(img1, (imgco[0]+400, imgco[1]))
    for i in range(0, row+1):
        tmp = ""
        for j in range(0, len(td[i])):
            tdl = list(td[i])
            if tdl[j] == ".":
                sleep(0.2)
            else:
                sleep(0.08)
            if tdl[j] == "-":
                if textstart == 5:
                    if con == "bk":
                        sound.bluesquawk()
                    elif con == "ti":
                        sound.keasquawk()
                    elif con == "tu":
                        sound.roboturkey()
                    textstart = imgco[0]+400
                    tmp = ""
                else:
                    textstart = 5
                    tmp = ""
                    if con == "bk":
                        sound.bluesquawk()
                    elif con == "ti":
                        sound.tiger()
                    elif con == "tu":
                        sound.keasquawk()
                tdl[j] = ""
            tmp += tdl[j]
            st.blit(hudfont.render(tmp, 1, (0,0,0)),(textstart,20*i+40))
            text_img = st
    st.fill((255,255,255))
    text_img = 0

def timer():
    global timerrender
    timerrender = hudfonttimer.render(str(levels.timers), 0, (0,0,0))