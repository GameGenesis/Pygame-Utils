import pygame

class Window:
    def __init__(self, size: pygame.Vector2 | tuple[int, int], caption: str="Game") -> None:
        pygame.init()
        pygame.display.set_caption(caption)
        self.surface = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
    
    @staticmethod
    def get_delta_time(clock_ticks):
        return float(clock_ticks) / 1000.0