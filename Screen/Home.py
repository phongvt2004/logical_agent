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
        self.button1 = ImageButton("./Assets/inputs/map1.png", 0.25)
        self.button2 = ImageButton("./Assets/inputs/map2.png", 0.25)
        self.button3 = ImageButton("./Assets/inputs/map3.png", 0.25)
        self.button4 = ImageButton("./Assets/inputs/map4.png", 0.25)
        self.button5 = ImageButton("./Assets/inputs/map5.png", 0.25)

    def handle_map(self, inp: int) -> callable:
        def handle() -> None:
            if inp == 1:
                map_file = "./map1.txt"
                output_file = "./out1.txt"
                pass
            elif inp == 2:
                map_file = "./map2.txt"
                output_file = "./out2.txt"
                pass
            elif inp == 3:
                map_file = "./map3.txt"
                output_file = "./out3.txt"
                pass
            elif inp == 4:
                map_file = "./map4.txt"
                output_file = "./out4.txt"
                pass
            elif inp == 5:
                map_file = "./map5.txt"
                output_file = "./out5.txt"
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

            self.button1.draw(self.screen, 400, 300, self.handle_map(1))
            self.button2.draw(self.screen, 600, 300, self.handle_map(2))
            self.button3.draw(self.screen, 800, 300, self.handle_map(3))
            self.button4.draw(self.screen, 1000, 300, self.handle_map(4))
            self.button5.draw(self.screen, 1200, 300, self.handle_map(5))

            pygame.display.update()
