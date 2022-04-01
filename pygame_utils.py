from abc import abstractmethod
import gc

import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2

class ButtonManager:
    def __init__(self) -> None:
        self.buttons = []
        for obj in gc.get_objects():
            if isinstance(obj, Button):
                self.buttons.append(obj)

    def handle_button_events(self, event, *args):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.rect.collidepoint(pos) and not button.disabled:
                    button.button_press()
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.button_release()
                if button.rect.collidepoint(pos) and not button.disabled:
                    button.call_back(*args)


class Button:
    def __init__(self, on_click=None, position=Vector2(0, 0), size=Vector2(150, 75), color=(255, 255, 255), hover_color=(220, 220, 220), pressed_color=(185, 185, 185), disabled_color=(165, 165, 165), border_radius=0, disabled=False, label=None, label_alignment="center"):
        self.func = on_click
        self.position = position
        self.size = size
        self.rect = pygame.rect.Rect(position, size)
        self.current_color = color
        self.color = color
        self.hover_color = hover_color
        self.pressed_color = pressed_color
        self.disabled_color = disabled_color
        self.border_radius = border_radius
        self.pressed = False
        self.set_disabled(disabled)
        self.label = label
        self.label_alignment = label_alignment
        self.set_label_pos()
        if self.label:
            self.label._render()

    def set_disabled(self, disabled):
        self.disabled = disabled
        self.current_color = self.disabled_color

    def set_label_pos(self):
        if self.label_alignment == "center":
            label_offset = (self.size.x / 2, self.size.y / 2)
        else:
            label_offset = (0, 0)
        label_pos = (self.position.x + self.label.position[0] + label_offset[0], self.position.y + self.label.position[1] + label_offset[1])
        self.label.set_position(label_pos, anchor="center")

    def set_text(self, text):
        if self.label:
            self.label.set_text(text)

    def draw(self, surface):
        self.mouseover()
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=self.border_radius)
        if self.label:
            self.label.draw(surface)

    def mouseover(self):
        if self.disabled or self.pressed:
            return
        self.current_color = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color

    def button_press(self):
        self.pressed = True
        self.current_color = self.pressed_color

    def button_release(self):
        self.pressed = False

    def call_back(self, *args):
        if self.func:
            return self.func(*args)


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