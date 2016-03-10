from pygame import *
import os

class Banana:
    def __init__(self):
        self.imgsrc = os.path.join("assets", "banana.png")
        self.img = image.load(self.imgsrc).convert_alpha()
        self.imgh = image.load(os.path.join("assets", "bananah.png")).convert_alpha()
    def render(self, mouseover):
        if not mouseover:
            return self.img
        else:
            return self.imgh
class Apple:
    def __init__(self):
        self.imgsrc = os.path.join("assets", "apple.png")
        self.img = image.load(self.imgsrc).convert_alpha()
        self.imgh = image.load(os.path.join("assets", "appleh.png")).convert_alpha()
    def render(self, mouseover):
        if not mouseover:
            return self.img
        else:
            return self.imgh
class Cookie:
    def __init__(self):
        self.imgsrc = os.path.join("assets", "cookie.png")
        self.img = image.load(self.imgsrc).convert_alpha()
        self.imgh = image.load(os.path.join("assets", "cookieh.png")).convert_alpha()
    def render(self, mouseover):
        if mouseover:
            return self.imgh
        else:
            return self.img

class Pie:
    def __init__(self):
        self.imgsrc = os.path.join("assets", "pie.png")
        self.img = image.load(self.imgsrc).convert_alpha()
        self.imgh = image.load(os.path.join("assets", "pieh.png")).convert_alpha()
    def render(self, mouseover):
        if mouseover:
            return self.imgh
        else:
            return self.img

class Windscreenwiper:
    def __init__(self):
        self.imgsrc = os.path.join("assets", "windscreenwiper.png")
        self.img = image.load(self.imgsrc).convert_alpha()
        self.imgh = image.load(os.path.join("assets", "windscreenwiperh.png")).convert_alpha()
    def render(self, mouseover):
        if mouseover:
            return self.imgh
        else:
            return self.img