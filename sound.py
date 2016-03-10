from pygame import *
import os


def collect1():
    snd = mixer
    snd.init()
    snd.music.load(os.path.join("assets", "sounds", "battle no1.ogg"))
    snd.music.play()

def collect2():
    snd = mixer
    snd.init()
    snd.music.load(os.path.join("assets", "sounds", "carpark music.ogg"))
    snd.music.play()

def turkeybattle():
    snd = mixer
    snd.init()
    snd.music.load(os.path.join("assets", "sounds", "battle no2.ogg"))
    snd.music.play(-1)

def tigerbattle():
    snd = mixer
    snd.init()
    snd.music.load(os.path.join("assets", "sounds", "tigerbattle.ogg"))
    snd.music.play(-1)

def tigergrowl():
    snd = mixer.Sound(os.path.join("assets", "sounds", "tigergrowl.ogg"))
    snd.stop()
    snd.set_volume(1)
    snd.play()

def bluesquawk():
    snd = mixer
    snd.init()
    snd.music.load(os.path.join("assets", "sounds", "bluekea squawk.ogg"))
    snd.music.play(-1)

def keasquawk():
    snd = mixer
    snd.init()
    snd.music.load(os.path.join("assets", "sounds", "kea squawk.ogg"))
    snd.music.play(-1)

def roboturkey():
    snd = mixer
    snd.init()
    snd.music.load(os.path.join("assets", "sounds", "robo-turkey.ogg"))
    snd.music.play(-1)

def tiger():
    snd = mixer
    snd.init()
    snd.music.load(os.path.join("assets", "sounds", "tiger.ogg"))
    snd.music.play(-1)