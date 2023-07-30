import pygame
from time import time
from typing import *

# Number type -> float or int
number = Union[float, int]

pygame.init()

class Config:
    rel  : list[int]        = [0, 0]
    scale: number           = 1
    font : pygame.font.Font = pygame.font.SysFont("Microsoft YaHei UI", 20)
    pause: bool             = False

class TrailPoint(tuple):
    def __init__(self, pos):
        tuple.__init__(self)
        self.pos = pos
        self.time = time()

    def __iter__(self):
        yield self.pos[0]
        yield self.pos[1]

    def get_time(self):
        return time() - self.time

class Star(pygame.sprite.Sprite):
    def __init__(self,
                 name:   str,
                 radius: number,
                 color:  Any,
                 x:      number,
                 y:      float,
                 vx:     number,
                 vy:     number,
                 mass:   number,
                 locked: bool = False
                 ):
        """
        A star
        :param name: name of star
        :param radius: radius of star
        :param color: color of star
        :param x: x pos of star
        :param y: y pos of star
        :param vx: x velocity of star
        :param vy: y velocity of star
        :param mass: mass of star
        :param locked: is star locked
        """
        pygame.sprite.Sprite.__init__(self)
        self.name  : str              = name
        self.x     : number           = x
        self.y     : number           = y
        self.vx    : number           = vx
        self.vy    : number           = vy
        self.mass  : number           = mass
        self.locked: bool             = locked
        self.radius: number           = radius
        self.color : Any              = color
        self.trail : list[TrailPoint] = []
        self.text  : pygame.Surface   = Config.font.render(self.name, False, (128, 128, 128))
        self.image:  pygame.Surface   = pygame.Surface((radius * 2, radius * 2)).convert_alpha()
        # Make it transparent
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, color, (radius, radius), radius, 0)
        self.rect:   pygame.Rect      = self.image.get_rect()
        self.flush()

    def __repr__(self):
        return self.name

    __str__ = __repr__

    @property
    def info(self):
        return self.x, self.y, self.vx, self.vy, self.mass

    def flush(self):
        self.rect.centerx = (self.x + Config.rel[0]) * Config.scale
        self.rect.centery = (self.y + Config.rel[1]) * Config.scale
        for point in self.trail:
            if point.get_time() > 1:
                self.trail.remove(point)

    def add_to_trail(self):
        self.trail.append(TrailPoint((self.x, self.y)))

class Message(pygame.sprite.Sprite):
    def __init__(self):
        """
        A message object
        """
        pygame.sprite.Sprite.__init__(self)
        self._text = ""
        self.flush((pygame.display.get_surface().get_width() - 10, 10))

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        pos = self.rect.topright
        self._text = text
        self.flush(pos)

    def flush(self, pos):
        """
        Flush image and rect attribute
        :param pos:
        :return:
        """
        self.image = Config.font.render(self._text, False, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topright = pos

class RightKey(pygame.sprite.Sprite):
    def __init__(self):
        """
        Right key menu
        """
        pygame.sprite.Sprite.__init__(self)
        # Each 30 px
        self.image = pygame.Surface((100, 30))
        self.items = [
            (self.text_surf("Pause"), self.pause)
        ]
        self.rect = self.image.get_rect()
        self.flush()

    @staticmethod
    def text_surf(text):
        return Config.font.render(text, False, (255, 255, 255))

    @staticmethod
    def pause():
        Config.pause = True

    def flush(self):
        """
        Flush sprite
        :return: None
        """
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            return
        hover_y = pygame.mouse.get_pos()[1] - self.rect.top
        y = 0
        for item in self.items:
            self.image.fill((0, 0, 0))
            if y < hover_y < y + 30:
                surf = pygame.Surface((self.image.get_width(), 30))
                surf.fill((0, 0, 255))
                surf.blit(item[0], (0, 0))
                item = (surf, item[1])
            self.image.blit(item[0], (0, y))
            y += 30
        if pygame.mouse.get_pressed():
            # is user pressed left mouse button key?
            # if it's true, then do function
            index = hover_y // 30
            self.items[index][1]()
