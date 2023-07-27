import pygame
from time import time
from typing import *

# number type -> float or int
number = Union[float, int]

pygame.init()

class GameConfig:
    rel: list[int]         = [0, 0]
    scale: number          = 1
    font: pygame.font.Font = pygame.font.SysFont("Microsoft YaHei UI", 20)

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
        self.text  : pygame.Surface   = GameConfig.font.render(self.name, False, (128, 128, 128))
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
        self.rect.centerx = (self.x + GameConfig.rel[0]) * GameConfig.scale
        self.rect.centery = (self.y + GameConfig.rel[1]) * GameConfig.scale
        for point in self.trail:
            if point.get_time() > 1:
                self.trail.remove(point)

    def add_to_trail(self):
        self.trail.append(TrailPoint((self.x, self.y)))

class Message(pygame.sprite.Sprite):
    def __init__(self, text, pos):
        pygame.sprite.Sprite.__init__(self)
        self._text = text
        self.flush(pos)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        pos = self.rect.topright
        self._text = text
        self.flush(pos)

    def flush(self, pos):
        self.image = GameConfig.font.render(self._text, False, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topright = pos
