import pygame
from Constant import Color


class Screen:
    def __init__(self,
                 screen: pygame.Surface,
                 height: int,
                 width: int,
                 font: pygame.font.Font,
                 background: str = None
                 ) -> None:
        self.screen = screen
        self.running = True
        self.SCREEN_HEIGHT = height
        self.SCREEN_WIDTH = width

        if background:
            self.background = pygame.image.load(background)
            self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        else:
            self.background = None

        self.font = font

    def draw_background(self) -> None:
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(Color.BLACK)

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()
