from abc import abstractmethod
import gc
import sys
from turtle import onclick, pos
from typing import Any, Callable, Optional

import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2


class EventManager:
    def __init__(self, call_backs: Optional[Callable] | Optional[list[Callable]]=None) -> None:
        self.button_manager = ButtonManager()
        if call_backs:
            if type(call_backs) == list:
                self.funcs = call_backs
            else:
                self.funcs = [call_backs]
        else:
            self.funcs = []

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for func in self.funcs:
                func(event)
            self.button_manager.handle_button_events(event)


class ButtonManager:
    def __init__(self) -> None:
        self.buttons = []
        for obj in gc.get_objects():
            if isinstance(obj, Button):
                self.buttons.append(obj)

    def handle_button_events(self, event: pygame.event.Event, *args) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button != 1:
                return
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.rect.collidepoint(pos) and not button.disabled:
                    button.button_press()
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button != 1:
                return
            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.button_release()
                if button.rect.collidepoint(pos) and not button.disabled:
                    button.call_back(*args)


class Button:
    def __init__(self, on_click:Optional[Callable]=None, 
    position: Vector2=Vector2(0, 0), size: Vector2=Vector2(150, 75), 
    color: pygame.Color | tuple[int, int, int]=(255, 255, 255), hover_color: pygame.Color | tuple[int, int, int]=(220, 220, 220), 
    pressed_color: pygame.Color | tuple[int, int, int]=(185, 185, 185), disabled_color: pygame.Color | tuple[int, int, int]=(165, 165, 165), 
    border_radius: int=0, disabled: bool=False, label: "Label"=None, label_alignment: str="center") -> None:
        self.func = on_click
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)
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

    def set_disabled(self, disabled: bool=True):
        self.disabled = disabled
        self.current_color = self.disabled_color

    def set_label_pos(self):
        if not self.label:
            return
        
        if self.label_alignment == "center":
            label_offset = (self.size.x / 2, self.size.y / 2)
        else:
            label_offset = (0, 0)
        label_pos = (self.position.x + self.label.position[0] + label_offset[0], self.position.y + self.label.position[1] + label_offset[1])
        self.label.set_position(label_pos, anchor="center")

    def set_text(self, text: str | Any):
        if self.label:
            self.label.set_text(text)

    def draw(self, surface: pygame.Surface):
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


class CheckBox(Button):
    def __init__(self, on_click:Optional[Callable]=None, 
    position: Vector2=Vector2(0, 0), size: Vector2=Vector2(50, 50), 
    color: pygame.Color | tuple[int, int, int]=(255, 255, 255), hover_color: pygame.Color | tuple[int, int, int]=(220, 220, 220), 
    pressed_color: pygame.Color | tuple[int, int, int]=(185, 185, 185), disabled_color: pygame.Color | tuple[int, int, int]=(165, 165, 165), 
    tick_color: pygame.Color | tuple[int, int, int]=(55, 55, 55), is_on: bool=False, 
    border_radius: int=0, disabled: bool=False, label_alignment: str="center") -> None:
        super().__init__(on_click, position, size, color, hover_color, pressed_color, disabled_color, 
        border_radius, disabled, None, label_alignment)
        self.tick_color = tick_color
        self.is_on = is_on
        self.tick_rect = pygame.Rect(Vector2(position.x + size.x/4, position.y + size.y/4), Vector2(size.x / 2, size.y / 2))
    
    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        if self.is_on:
            pygame.draw.rect(surface=surface, color=self.tick_color, rect=self.tick_rect)

    def call_back(self, *args):
        self.is_on = not self.is_on
        super().call_back(self.is_on, *args)


class Label(Sprite):
    def __init__(self, text: str | Any, color: pygame.Color | tuple[int, int, int]=(255, 255, 255), 
    font_name: str=None, font_size: int=28, position: tuple[int, int]=(0, 0), anchor: str="topleft"):
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

    def clip(self, rect: pygame.Rect):
        self.image = self.image.subsurface(rect)
        self.rect = self.image.get_rect(**{self.anchor: self.position})

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def set_text(self, text: str):
        self.text = str(text)
        self._render()

    def set_font(self, font_name: str, font_size: int):
        self.font = pygame.font.Font(font_name, font_size)
        self._render()

    def set_color(self, color: tuple[int, int, int]):
        self.color = color
        self._render()

    def set_position(self, position: tuple[int, int], anchor: str=None):
        self.position = position
        if anchor:
            self.anchor = anchor

        self.rect = self.image.get_rect(**{self.anchor: self.position})


class Shape(object):
    def __init__(self, pos: Vector2=Vector2(0, 0), color: pygame.Color | tuple[int, int, int]=(0, 0, 0)) -> None:
        self.pos = pos
        self.color = color

    @abstractmethod
    def move(self, x: int=None, y: int=None):
        ...

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        ...


class Square(Shape):
    def __init__(self, pos: Vector2=Vector2(0, 0), color: pygame.Color | tuple[int, int, int]=(0, 0, 0), 
    size: Vector2=Vector2(100, 100)) -> None:
        super().__init__(pos, color)
        self.size = size
        self.rect = pygame.Rect(pos, size)

    def move(self, x: int=None, y: int=None):
        if x and y:
            self.pos = pygame.Rect(self.pos, Vector2(x, y))
        elif x:
            self.pos = pygame.Rect(self.pos, Vector2(x, self.pos.y))
        else:
            self.pos = pygame.Rect(self.pos, Vector2(self.pos.x, y))

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface=surface, color=self.color, rect=self.rect)


class Circle(Shape):
    def __init__(self, pos: Vector2=Vector2(0, 0), color: pygame.Color | tuple[int, int, int]=(0, 0, 0), radius: int=10) -> None:
        super().__init__(pos, color)
        self.radius = radius

    def move(self, x: int=None, y: int=None):
        if x and y:
            self.pos = Vector2(x, y)
        elif x:
            self.pos = Vector2(x, self.pos.y)
        else:
            self.pos = Vector2(self.pos.x, y)

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface=surface, color=self.color, center=self.pos, radius=self.radius)


class Color:
    BLACK = pygame.color.Color(0, 0, 0)
    CLEAR = pygame.color.Color(0, 0, 0, 0)
    WHITE = pygame.color.Color(255, 255, 255)
    GREY = pygame.color.Color(128, 128, 128)
    GRAY = GREY

    GREEN = pygame.color.Color(0, 255, 0)
    BLUE = pygame.color.Color(0, 0, 255)
    CYAN = pygame.color.Color(0, 255, 255)
    RED = pygame.color.Color(255, 0, 0)
    PINK = pygame.color.Color(255, 102, 178)
    YELLOW = pygame.color.Color(255, 255, 0)
    ORANGE = pygame.color.Color(255, 128, 0)
    MAGENTA = pygame.color.Color(255, 0, 255)