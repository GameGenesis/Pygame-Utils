from abc import abstractmethod

import pygame
from pygame import Vector2


class Shape(object):
    def __init__(self, position: Vector2=Vector2(0, 0), color: pygame.Color | tuple[int, int, int]=(0, 0, 0)) -> None:
        self.position = position
        self.color = color

    @abstractmethod
    def move(self, x: int=None, y: int=None):
        ...

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        ...


class Square(Shape):
    def __init__(self, position: Vector2=Vector2(0, 0), size: Vector2=Vector2(100, 100),
    color: pygame.Color | tuple[int, int, int]=(0, 0, 0)) -> None:
        super().__init__(position, color)
        self.size = size
        self.rect = pygame.Rect(position, size)

    def move(self, x: int=None, y: int=None):
        if x and y:
            self.position = pygame.Rect(self.position, Vector2(x, y))
        elif x:
            self.position = pygame.Rect(self.position, Vector2(x, self.position.y))
        else:
            self.position = pygame.Rect(self.position, Vector2(self.position.x, y))

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface=surface, color=self.color, rect=self.rect)


class Circle(Shape):
    def __init__(self, position: Vector2=Vector2(0, 0), radius: int=10, color: pygame.Color | tuple[int, int, int]=(0, 0, 0)) -> None:
        super().__init__(position, color)
        self.radius = radius

    def move(self, x: int=None, y: int=None):
        if x and y:
            self.position = Vector2(x, y)
        elif x:
            self.position = Vector2(x, self.position.y)
        else:
            self.position = Vector2(self.position.x, y)

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface=surface, color=self.color, center=self.position, radius=self.radius)
