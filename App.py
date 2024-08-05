import pygame
from Screen import Screen
from Constant import Setting


class Window:
    def __init__(self) -> None:
        pygame.init()
        self.setup_attributes()
        pygame.display.set_caption("Delivery system")

    def setup_attributes(self) -> None:
        self.SCREEN_HEIGHT = Setting.HEIGHT
        self.SCREEN_WIDTH = Setting.WIDTH

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        font_url = "./Assets/Poppins.ttf"
        self.text_font = pygame.font.Font(font_url, 40)

    def run(self) -> None:
        Screen.Screen(self.screen, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.text_font).run()
        pygame.quit()


if __name__ == "__main__":
    app = Window()
    app.run()
