import pygame

from Agent import Agent
from Cell import get_percept
from Program import Program
from Screen.Screen import Screen
from Component.Text import Text
from Constant import Color
from Component.Button import ImageButton


class Main(Screen):
    def __init__(self, inp: str, output: str, *args):
        super(Main, self).__init__(*args)
        self.program = Program(inp)
        self.agent = Agent(self.program, output)
        self.actions = self.agent.solve_wumpus_world()
        self.cell_w = 110
        self.cell_h = 60
        self.grid_w = self.cell_w * len(self.program.map_matrix)
        self.grid_h = self.cell_h * len(self.program.map_matrix)

        font_url = "./Assets/Poppins.ttf"
        self.font = pygame.font.Font(font_url, 20)

    def drawRect(self, x: int, y: int, color: tuple, color_mode: int = 0) -> None:
        rect = pygame.Rect(x, y, self.cell_w, self.cell_h)
        pygame.draw.rect(self.screen, color, rect, color_mode)

    def drawTextCell(self, text: str, x: int, y: int, txt_color: tuple, bg_color: tuple) -> None:
        self.drawRect(x, y, bg_color, 1)
        rect = pygame.Rect(x, y, self.cell_w, self.cell_h)

        text = self.font.render(text, True, txt_color)
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)

    def drawCell(self, value: list[bool], x: int, y: int) -> None:
        text = ''
        for i in range(len(value)):
            if value[i]:
                text += get_percept(i) + ' '

        self.drawTextCell(text, x, y, Color.WHITE, Color.WHITE)

    def drawGrid(self, start_x: int, start_y: int):
        end_x = start_x + self.grid_w
        end_y = start_y + self.grid_h

        for x in range(start_x, end_x, self.cell_w):
            for y in range(start_y, end_y, self.cell_h):
                pos_x = (x - start_x) // self.cell_w
                pos_y = (y - start_y) // self.cell_h

                self.drawCell(self.program.cell_matrix[pos_x][pos_y].percept, x, y)

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.draw_background()
            self.drawGrid(50, 50)

            pygame.display.update()
