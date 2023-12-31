from __future__ import annotations

import pygame
from time import time
from typing import *

# Number type -> float or int
number = Union[float, int]

pygame.init()

class Config:
    rel  : list[int, ...]   = [0, 0]
    scale: number           = 1
    font : pygame.font.Font = pygame.font.SysFont("Microsoft YaHei UI", 20)
    pause: bool             = False
    speed: number           = 2

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
                 y:      number,
                 z:      number,
                 vx:     number,
                 vy:     number,
                 vz:     number,
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
        self.z     : number           = z
        self.vx    : number           = vx
        self.vy    : number           = vy
        self.vz    : number           = vz
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

    def __str__(self):
        vars = (
            self.name,   self.x,      self.y,    self.z,
            self.vx,     self.vy,     self.vz,   self.mass,
            self.locked, self.radius, self.color
        )
        return f"Sprite{vars}"

    @property
    def info(self):
        return self.x, self.y, self.z, self.vx, self.vy, self.vz, self.mass

    def flush(self):
        self.rect.centerx = (self.x + Config.rel[0]) * Config.scale
        self.rect.centery = (self.y + Config.rel[1]) * Config.scale
        for point in self.trail:
            if point.get_time() > 1:
                self.trail.remove(point)

    def add_to_trail(self):
        self.trail.append(TrailPoint((self.x, self.y, self.z)))

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
    def text(self, text: str):
        pos = self.rect.topright
        self._text = text
        self.flush(pos)

    def flush(self, pos: Iterable[number]):
        """
        Flush image and rect attribute
        :param pos: message's topright
        :return: None
        """
        self.image = Config.font.render(self._text, False, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topright = pos

class Button(pygame.sprite.Sprite):
    count = 0

    def __init__(
        self,
        img_name: str,
        callback: Any,
        title   : str          = "",
        pos     : tuple[int, ] = None
    ):
        """
        A button that shows on sidebar.
        :param img_name: the image path of button
        :param callback: function that will be called when button is clicked
        :param title: text that will be shown when mouse hovers on the button
        :param pos: position of star. If not given, use id (sidebar pos)
        """
        pygame.sprite.Sprite.__init__(self)
        self._title    = title
        self.func      = callback
        self.text_surf = Config.font.render(title, False, (255, 255, 255), (64, 64, 64))
        size           = self.text_surf.get_size()
        self.prompt    = pygame.Surface((size[0] + 20, size[1]))
        self.prompt.fill((64, 64, 64))
        self.prompt.blit(self.text_surf, (10, 0))
        self.image = pygame.image.load(img_name)
        self.rect = self.image.get_rect()
        if pos is None:
            self._id       = self.count
            Button.count  += 1
            self.rect.topleft = (1010, self._id * 50 + 10)
        else:
            self.rect.topleft = pos

    def __call__(self):
        self.func()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        self.text_surf = Config.font.render(title, False, (255, 255, 255), (64, 64, 64))
        size           = self.text_surf.get_size()
        self.prompt    = pygame.Surface((size[0] + 20, size[1]))
        self.prompt.fill((64, 64, 64))
        self.prompt.blit(self.text_surf, (10, 0))

    def is_hover(self) -> bool:
        """
        Judge is mouse hovering on this button
        :return: boolean
        """
