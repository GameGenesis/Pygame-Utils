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

class Square(Shape):
    def __init__(self, pos: Vector2=Vector2(0, 0), color: tuple[int]=(0, 0, 0), size: Vector2=Vector2(100, 100)) -> None:
        super().__init__(pos, color)
        self.size = size
        self.rect = pygame.Rect(pos, size)

    def move(self, x=None, y=None):
        if x and y:
            self.pos = pygame.Rect(self.pos, Vector2(x, y))
        elif x:
            self.pos = pygame.Rect(self.pos, Vector2(x, self.pos.y))
        else:
            self.pos = pygame.Rect(self.pos, Vector2(self.pos.x, y))

    def draw(self, surface):
        pygame.draw.rect(surface=surface, color=self.color, rect=self.rect)

class Circle(Shape):
    def __init__(self, pos: Vector2=Vector2(0, 0), color: tuple[int]=(0, 0, 0), radius: int=10) -> None:
        super().__init__(pos, color)
        self.radius = radius

    def move(self, x=None, y=None):
        if x and y:
            self.pos = Vector2(x, y)
        elif x:
            self.pos = Vector2(x, self.pos.y)
        else:
            self.pos = Vector2(self.pos.x, y)

    def draw(self, surface):
        pygame.draw.circle(surface=surface, color=self.color, center=self.pos, radius=self.radius)
