import pygame
from Screen.Screen import Screen
from Component.Text import Text
from Constant import Color
from Component.Button import ImageButton
from Screen.Main import Main


class Home(Screen):
    def __init__(self, *args):
        super(Home, self).__init__(*args)
        self.title = Text("Choose map to continue", self.font, Color.WHITE)
        self.button1 = ImageButton("./Assets/inputs/input1.png", 0.25)
        self.button2 = ImageButton("./Assets/inputs/input2.png", 0.25)

    def handle_map(self, inp: int) -> callable:
        def handle() -> None:
            if inp == 1:
                map_file = "./map1.txt"
                output_file = "./out1.txt"
                pass
            elif inp == 2:
                map_file = "./map2.txt"
                output_file = "./out1.txt"
                pass
            else:
                return

            Main(map_file, output_file, self.screen, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.font, self.background).run()

        return handle

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.draw_background()
            self.title.show(self.screen, self.SCREEN_WIDTH // 2, 150)

            self.button1.draw(self.screen, self.SCREEN_WIDTH // 2, 300, self.handle_map(1))
            self.button2.draw(self.screen, self.SCREEN_WIDTH // 2, 370, self.handle_map(2))

            pygame.display.update()
