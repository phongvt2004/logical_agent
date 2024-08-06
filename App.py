import pygame
from Screen import Home
from Constant import Setting


class Window:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Delivery system")

        self.SCREEN_HEIGHT = Setting.HEIGHT
        self.SCREEN_WIDTH = Setting.WIDTH

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        font_url = "./Assets/Poppins.ttf"
        self.text_font = pygame.font.Font(font_url, 40)

        self.background = "./Assets/background.jpg"

    def run(self) -> None:
        Home.Home(self.screen, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.text_font, self.background).run()
        pygame.quit()


if __name__ == "__main__":
    app = Window()
    app.run()
