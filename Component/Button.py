import pygame
from Component import Component
from typing import Callable


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


class ImageButton(Button):
    def __init__(self, image: str, scale: float = 1) -> None:
        super(ImageButton, self).__init__()
        btn_img = pygame.image.load(image)
        btn_img = btn_img.convert_alpha()

        width = btn_img.get_width()
        height = btn_img.get_height()
        self.image = pygame.transform.scale(btn_img, (int(width * scale), int(height * scale)))

    def draw(self, screen: pygame.Surface, x: int, y: int, action: Callable) -> None:
        rect = self.image.get_rect()
        rect.topleft = (x - self.image.get_width() // 2, y)

        if self.is_clicked(rect):
            action()

        screen.blit(self.image, (rect.x, rect.y))
