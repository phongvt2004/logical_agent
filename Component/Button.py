import pygame
from Component import Component


class Button(Component.Component):
    def __init__(self) -> None:
        super().__init__()
        self.clicked = False
        self.mouse_down_in_rect = False

    def is_clicked(self, rect: pygame.Rect) -> bool:
        pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if rect.collidepoint(pos):
            if mouse_pressed == 1 and not self.mouse_down_in_rect:
                self.mouse_down_in_rect = True
            elif mouse_pressed == 0 and self.mouse_down_in_rect:
                self.mouse_down_in_rect = False
                self.clicked = True
                return True
        else:
            self.mouse_down_in_rect = False

        return False

    def show(self, screen: pygame.Surface, x: int, y: int) -> None:
        pass
