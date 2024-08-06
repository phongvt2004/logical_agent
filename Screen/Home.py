import pygame
from Screen.Screen import Screen
from Component.Text import Text
from Constant import Color
from Component.Button import ImageButton


class Home(Screen):
    def __init__(self, *args):
        super(Home, self).__init__(*args)
        self.title = Text("Choose input to continue", self.font, Color.WHITE)
        self.button1 = ImageButton("./Assets/inputs/input1.png", 0.25)
        self.button2 = ImageButton("./Assets/inputs/input2.png", 0.25)
        self.button3 = ImageButton("./Assets/inputs/input3.png", 0.25)
        self.button4 = ImageButton("./Assets/inputs/input4.png", 0.25)
        self.button5 = ImageButton("./Assets/inputs/input5.png", 0.25)

    def handleInput(self, input: int) -> callable:
        def handle() -> None:
            if input == 1:
                pass
            elif input == 2:
                pass
            elif input == 3:
                pass
            elif input == 4:
                pass
            elif input == 5:
                pass

        return handle

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.draw_background()
            self.title.show(self.screen, self.SCREEN_WIDTH // 2, 100)

            self.button1.draw(self.screen, self.SCREEN_WIDTH // 2, 200, self.handleInput(1))
            self.button2.draw(self.screen, self.SCREEN_WIDTH // 2, 270, self.handleInput(2))
            self.button3.draw(self.screen, self.SCREEN_WIDTH // 2, 340, self.handleInput(3))
            self.button4.draw(self.screen, self.SCREEN_WIDTH // 2, 410, self.handleInput(4))
            self.button5.draw(self.screen, self.SCREEN_WIDTH // 2, 480, self.handleInput(5))

            pygame.display.update()
