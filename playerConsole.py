from buffalo.tray import Tray
from buffalo import utils
from itertools import chain
import pygame
import random

class PlayerConsole:
    TEXT_EVENTS = list()
    ALPHA = 255
    ALPHA_WAIT = 100
    ALPHA_DECAY = 10
    ALPHA_COUNTER = 5001

    @staticmethod
    def init():
        PlayerConsole.tray = Tray(
            (10,utils.SCREEN_H - utils.SCREEN_H / 4 - 75),
            (utils.SCREEN_W / 2, utils.SCREEN_H / 4),
            color=(100,100,100,240))
        PlayerConsole.registerNewEvent("Hello!")
        PlayerConsole.registerNewEvent("Hello!")
        PlayerConsole.registerNewEvent("Hello!")
        ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum lobortis ac enim vel feugiat. Duis ac metus id est lobortis euismod. Vestibulum finibus est eget odio rhoncus consequat. Vestibulum sed lectus justo. Aenean fringilla mi et ultricies condimentum. Donec sapien quam, congue vitae felis at, bibendum tincidunt purus. Nulla in nunc consequat, laoreet nibh non, pulvinar eros. Quisque at justo mauris."
        PlayerConsole.registerNewEvent(ipsum,(0,255,0,255))

    @staticmethod
    def registerNewEvent(text,color=(0,0,0,255)):
        newEvent = EventText('-'+text,color)
        PlayerConsole.TEXT_EVENTS.append(newEvent)
        PlayerConsole.flashOn()

    @staticmethod
    def flashOn():
        PlayerConsole.ALPHA = 255
        PlayerConsole.ALPHA_COUNTER = 0
        PlayerConsole.tray.render()
        PlayerConsole.render()

    @staticmethod
    def update():
        if PlayerConsole.ALPHA is 255:
            PlayerConsole.ALPHA_COUNTER += 1
        if PlayerConsole.ALPHA_COUNTER > PlayerConsole.ALPHA_WAIT and PlayerConsole.ALPHA > 0:
            PlayerConsole.ALPHA -= PlayerConsole.ALPHA_DECAY
            PlayerConsole.render()
        if PlayerConsole.ALPHA < 0:
            PlayerConsole.ALPHA = 0
            PlayerConsole.tray.surface = utils.empty_surface((1,1))
        
        #Stress Test Debugging Call:
        #PlayerConsole.registerNewEvent(str(random.random()))


    @staticmethod
    def render():
        totalHeight = 0
        #PlayerConsole.tray.update()
        texts = list()
        for textMessage in reversed(PlayerConsole.TEXT_EVENTS):
            myfont = pygame.font.SysFont("monospace", 15)
            thisMessage = list()
            for line in TextWrapper.wrap_line(textMessage.text, myfont, PlayerConsole.tray.size[0]):
                label = myfont.render(line, True, textMessage.color)
                totalHeight += label.get_height()
                thisMessage.append(label)
            texts.extend(reversed(thisMessage))
            if totalHeight > PlayerConsole.tray.surface.get_height():
                break
        if totalHeight > PlayerConsole.tray.surface.get_height():
            totalHeight = PlayerConsole.tray.surface.get_height()

        newSurface = utils.empty_surface((PlayerConsole.tray.surface.get_width(), totalHeight))
        currHeight = 0
        for textSurface in texts:
            newSurface.blit(textSurface,(0,newSurface.get_height() - currHeight - textSurface.get_height()))
            currHeight += textSurface.get_height()
            if currHeight > PlayerConsole.tray.surface.get_height():
                break
        PlayerConsole.tray.render()
        PlayerConsole.tray.surface.blit(newSurface,(0,PlayerConsole.tray.surface.get_height() - newSurface.get_height()))
        pixels_alpha = pygame.surfarray.pixels_alpha(PlayerConsole.tray.surface)
        pixels_alpha[...] = (pixels_alpha * (PlayerConsole.ALPHA / 255.0))
        del pixels_alpha


class EventText:
    def __init__(self, text, color=(0,0,0,255)):
        self.text = text
        self.color = color

#Code referenced from https://pygame.org/wiki/TextWrapping
class TextWrapper:
    @staticmethod
    def truncate_line(text, font, maxWidth):
        real = len(text)
        stext = text
        l = font.size(text)[0]
        cut = 0
        a = 0
        done = 1
        old = None
        while l > maxWidth:
            a += 1
            n = text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext = n[:-cut]
            else:
                stext = n
            l = font.size(stext)[0]
            real = len(stext)
            done = 0
        return real, done, stext

    @staticmethod
    def wrap_line(text, font, maxWidth):
        done = 0
        wrapped = list()

        while not done:
            nl, done, stext = TextWrapper.truncate_line(text, font, maxWidth)
            wrapped.append(stext.strip())
            text = text[nl:]
        return wrapped
