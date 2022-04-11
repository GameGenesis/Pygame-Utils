from abc import abstractmethod

import pygame
from pygame import Vector2


class Shape(object):
    def __init__(self, position: Vector2 | tuple[int, int]=Vector2(0, 0), color: pygame.Color | tuple[int, int, int]=(0, 0, 0)) -> None:
        """
        Parameters
        ----------
        position : Vector2 | tuple[int, int]
            The position of the shape. Default is (0, 0)
        color : pygame.Color | tuple[int, int, int]
            The position of the shape. Default is black or (0, 0, 0)

        Returns
        -------
        None
        """
        self.position = position
        self.color = color

    @abstractmethod
    def move(self, x: int=None, y: int=None):
        ...

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        ...


class Square(Shape):
    def __init__(self, position: Vector2| tuple[int, int]=Vector2(0, 0), size: Vector2 | tuple[int, int]=Vector2(100, 100),
    color: pygame.Color | tuple[int, int, int]=(0, 0, 0)) -> None:
        """
        Parameters
        ----------
        position : Vector2 | tuple[int, int]
            The position of the shape. Default is (0, 0)
        size : Vector2 | tuple[int, int]
            The size of the square. Default is (100, 100)
        color : pygame.Color | tuple[int, int, int]
            The position of the shape. Default is black or (0, 0, 0)

        Returns
        -------
        None
        """
        super().__init__(position, color)
        self.size = size
        self.rect = pygame.Rect(position, size)

    def move(self, x: int=None, y: int=None) -> None:
        """
        Moves the shape to a specified x and y amount. If either axis is not specified, uses the shape's current position

        Parameters
        ----------
        x : int, optional
            The x position of the object. If not specified, uses the shape's current x position
        y : int, optional
            The y position of the object. If not specified, uses the shape's current y position

        Returns
        -------
        None
        """
        if x and y:
            self.position = pygame.Rect(self.position, Vector2(x, y))
        elif x:
            self.position = pygame.Rect(self.position, Vector2(x, self.position.y))
        else:
            self.position = pygame.Rect(self.position, Vector2(self.position.x, y))

    def draw(self, surface: pygame.Surface):
        """
        Draws the shape to a surface

        Parameters
        ----------
        surface : Surface
            The surface to draw the shape on

        Returns
        -------
        None
        """
        pygame.draw.rect(surface=surface, color=self.color, rect=self.rect)


class Circle(Shape):
    def __init__(self, position: Vector2=Vector2(0, 0), radius: int=10, color: pygame.Color | tuple[int, int, int]=(0, 0, 0)) -> None:
        """
        Parameters
        ----------
        position : Vector2 | tuple[int, int]
            The position of the shape. Default is (0, 0)
        radius : int
            The radius of the circle. Default is 10
        color : pygame.Color | tuple[int, int, int]
            The position of the shape. Default is black or (0, 0, 0)

        Returns
        -------
        None
        """
        super().__init__(position, color)
        self.radius = radius

    def move(self, x: int=None, y: int=None):
        """
        Moves the shape to a specified x and y amount. If either axis is not specified, uses the shape's current position

        Parameters
        ----------
        x : int, optional
            The x position of the object. If not specified, uses the shape's current x position
        y : int, optional
            The y position of the object. If not specified, uses the shape's current y position

        Returns
        -------
        None
        """
        if x and y:
            self.position = Vector2(x, y)
        elif x:
            self.position = Vector2(x, self.position.y)
        else:
            self.position = Vector2(self.position.x, y)

    def draw(self, surface: pygame.Surface):
        """
        Draws the shape to a surface

        Parameters
        ----------
        surface : Surface
            The surface to draw the shape on

        Returns
        -------
        None
        """
        pygame.draw.circle(surface=surface, color=self.color, center=self.position, radius=self.radius)
