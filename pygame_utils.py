from abc import abstractmethod
import gc

import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2


class Label(Sprite):
    def __init__(self, text, color=(255, 255, 255), font_name=None, font_size=28, position=(0, 0), anchor="topleft"):
        super().__init__()
        self.font = pygame.font.Font(font_name, font_size)
        self.text = str(text)
        self.color = color
        self.anchor = anchor
        self.position = position
        self._render()

    def _render(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(**{self.anchor: self.position})

    def clip(self, rect):
        self.image = self.image.subsurface(rect)
        self.rect = self.image.get_rect(**{self.anchor: self.position})

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def set_text(self, text):
        self.text = str(text)
        self._render()

    def set_font(self, font_name, font_size):
        self.font = pygame.font.Font(font_name, font_size)
        self._render()

    def set_color(self, color):
        self.color = color
        self._render()

    def set_position(self, position, anchor=None):
        self.position = position
        if anchor:
            self.anchor = anchor

        self.rect = self.image.get_rect(**{self.anchor: self.position})


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


class Color:
    BLACK = pygame.color.Color(0, 0, 0)
    CLEAR = pygame.color.Color(0, 0, 0, 0)
    WHITE = pygame.color.Color(255, 255, 255)
    GREY = pygame.color.Color(128, 128, 128)
    GRAY = GREY

    GREEN = pygame.color.Color(0, 255, 0)
    BLUE = pygame.color.Color(0, 0, 255)
    BLUE = pygame.color.Color(0, 255, 255)
    RED = pygame.color.Color(255, 0, 0)
    PINK = pygame.color.Color(255, 102, 178)
    YELLOW = pygame.color.Color(255, 255, 0)
    ORANGE = pygame.color.Color(255, 128, 0)
    MAGENTA = pygame.color.Color(255, 0, 255)