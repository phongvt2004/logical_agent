import pygame
from Component import Component


class Text(Component.Component):
    def __init__(self, text: str, font: pygame.font.Font, color: tuple) -> None:
        super().__init__()
        self.text = font.render(text, True, color)

    def show(self, screen: pygame.Surface, x: int, y: int) -> None:
        text_position = self.text.get_rect(center=(x, y))
        screen.blit(self.text, text_position)
