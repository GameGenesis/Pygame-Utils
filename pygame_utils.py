from abc import abstractmethod
import gc

import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2

class Shape(object):
    def __init__(self, pos: Vector2=Vector2(0, 0), color: tuple[int]=(0, 0, 0)) -> None:
        self.pos = pos
        self.color = color

    @abstractmethod
    def move(self, x=None, y=None):
        ...

    @abstractmethod
    def draw(self, surface):
        ...

