import pygame

class Component:
    def __init__(self) -> None:
        self.clicked = False
        self.mouse_down_in_rect = False

    def show(self, screen: pygame.Surface, x: int, y: int) -> None:
        pass
