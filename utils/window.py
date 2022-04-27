from typing import Optional
import pygame

class Window:
    def __init__(self, size: pygame.Vector2 | tuple[int, int], caption: Optional[str]="Game") -> None:
        pygame.init()
        pygame.display.set_caption(caption)
        return pygame.display.set_mode(size)
        