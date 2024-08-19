from time import sleep

import pygame

from Agent import Agent, Action
from Cell import get_percept
from Component.Component import Component
from Program import Program
from Screen.Screen import Screen
from Component.Text import Text
from Constant import Color
from Component.Button import ImageButton

class Image(Component):
    def __init__(self, url: str, scale: float, rotate: float = 0):
        image = pygame.image.load(url)
        image = image.convert_alpha()

        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.image = pygame.transform.rotate(self.image, rotate)

    def show(self, screen: pygame.Surface, x: int, y: int) -> None:
        width = self.image.get_width()
        height = self.image.get_height()
        screen.blit(self.image, (x - width // 2, y - height // 2))

def get_percept_icon(percept: str) -> str:
    base_url = "./Assets/characters/"
    if percept == "A":
        return f"{base_url}agent.png"
    elif percept == "P":
        return f"{base_url}pit.png"
    elif percept == "W":
        return f"{base_url}monster.png"
    elif percept == "H_P":
        return f"{base_url}healing.png"
    elif percept == "P_G":
        return f"{base_url}poisonous.png"
    elif percept == "G":
        return f"{base_url}treasure.png"
    return ""

class Main(Screen):
    def __init__(self, inp: str, output: str, *args):
        super(Main, self).__init__(*args)
        self.program = Program(inp)
        self.agent = Agent(self.program, output)
        self.actions, self.cell_matrix = self.agent.solve_wumpus_world()
        self.direction = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        self.current_direction = 0
        self.cell_w = 80
        self.cell_h = 80
        self.grid_w = self.cell_w * len(self.program.cell_matrix)
        self.grid_h = self.cell_h * len(self.program.cell_matrix)
        font_url = "./Assets/Poppins.ttf"
        self.font = pygame.font.Font(font_url, 15)
        self.agent_pos = (0, len(self.program.cell_matrix) - 1)
        self.state = 0
        self.shoot = Image("./Assets/characters/arrow.png", 0.015)
        self.current_action = ""
        self.score = 0
        self.HP = 100
        self.potion = 0
        self.robot = [
            Image(get_percept_icon("A"), 0.012),
            Image(get_percept_icon("A"), 0.012, 90),
            Image(get_percept_icon("A"), 0.012, 180),
            Image(get_percept_icon("A"), 0.012, 270)
        ]

    def turn_right(self):
        self.current_direction += 1
        self.current_direction %= len(self.direction)

    def turn_left(self):
        if self.current_direction == 0:
            self.current_direction = len(self.direction)
        self.current_direction -= 1

    def move_forward(self):
        self.agent_pos = tuple(map(lambda i, j: i + j, self.agent_pos, self.direction[self.current_direction]))

    def drawRect(self, x: int, y: int, color: tuple, color_mode: int = 0) -> None:
        rect = pygame.Rect(x, y, self.cell_w, self.cell_h)
        pygame.draw.rect(self.screen, color, rect, color_mode)

    def drawTextCell(self, text: str, x: int, y: int, txt_color: tuple, bg_color: tuple) -> None:
        self.drawRect(x, y, bg_color, 1)
        rect = pygame.Rect(x, y, self.cell_w, self.cell_h)
        pos = rect.center

        text = self.font.render(text, True, txt_color)
        text_rect = text.get_rect(center=(pos[0], pos[1] - 20))
        self.screen.blit(text, text_rect)

    def drawCell(self, value: list[bool], x: int, y: int) -> None:
        text = []
        obj = []
        ok = ['S', 'B', 'W_H', 'G_L']
        for (i, perc) in enumerate(value):
            if perc:
                percept = get_percept(i)
                if percept not in ok:
                    obj.append(percept)
                else:
                    text.append(percept)

        self.drawTextCell(', '.join(text), x, y, Color.WHITE, Color.WHITE)

        rect = pygame.Rect(x, y, self.cell_w, self.cell_h)
        pos = rect.center
        for (i, per) in enumerate(obj):
            img = Image(get_percept_icon(per), 0.01)
            if len(obj) == 1:
                pos_x = pos[0]
            elif i == 0:
                pos_x = pos[0] - 20
            else:
                pos_x = pos[0] + 20
            pos_y = pos[1] + 10 if len(text) else pos[1]
            img.show(self.screen, pos_x, pos_y)

    def draw_agent(self, x: int, y: int):
        rect = pygame.Rect(x, y, self.cell_w, self.cell_h)
        pos = rect.center
        self.robot[self.current_direction].show(self.screen, pos[0], pos[1])

    def drawGrid(self, start_x: int, start_y: int):
        end_x = start_x + self.grid_w
        end_y = start_y + self.grid_h

        for x in range(start_x, end_x, self.cell_w):
            for y in range(start_y, end_y, self.cell_h):
                pos_x = (x - start_x) // self.cell_w
                pos_y = (y - start_y) // self.cell_h

                if (pos_x, pos_y) == self.agent_pos and self.state < len(self.actions) - 1:
                    self.draw_agent(x, y)
                    self.drawCell(self.cell_matrix[pos_y][pos_x].percept, x, y)
                else:
                    self.drawRect(x, y, Color.GREY)
                    self.drawRect(x, y, Color.WHITE, 1)

        ladder = Image("./Assets/characters/ladder.png", 0.02)
        ladder.show(self.screen, 50, self.cell_h * len(self.cell_matrix) + 50)
        print(self.cell_h * (len(self.cell_matrix) - 1))

    def update_state(self):
        action = self.actions[self.state]
        print(action)
        self.current_action = f"Action: {action}"

        if action == Action.MOVE_FORWARD:
            pos = self.agent_pos
            if self.cell_matrix[pos[1]][pos[0]].exist_poisonousgas():
                self.HP -= 25
            self.move_forward()
            self.score -= 10
        elif action == Action.TURN_RIGHT:
            self.turn_right()
        elif action == Action.TURN_LEFT:
            self.turn_left()
        elif action == Action.GRAB_GOLD:
            self.score += 5000
            self.score -= 10
            pos = self.agent_pos
            self.cell_matrix[pos[1]][pos[0]].grab_gold()
        elif action == Action.GRAB_POTION:
            self.score -= 10
            self.potion += 1
            pos = self.agent_pos
            self.cell_matrix[pos[1]][pos[0]].grab_heal(cell_matrix=self.cell_matrix)
        elif action == Action.SHOOT:
            self.score -= 100
            pos = tuple(map(lambda i, j: i + j, self.agent_pos, self.direction[self.current_direction]))
            self.cell_matrix[pos[1]][pos[0]].kill_wumpus(self.cell_matrix)
        elif action == Action.CLIMB:
            self.score += 10
        elif action == Action.HEAL:
            self.score -= 10
            self.HP = min(100, self.HP + 25)
            self.potion -= 1

        self.cell_matrix[self.agent_pos[1]][self.agent_pos[0]].explore()
        self.state += 1

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.draw_background()
            self.drawGrid(50, 50)

            if self.state < len(self.actions) and self.actions[self.state] == Action.SHOOT:
                pos = tuple(map(lambda i, j: i + j, self.agent_pos, self.direction[self.current_direction]))
                print(pos[0] * self.cell_w + 50, pos[1] * self.cell_h + 50)
                self.shoot.show(self.screen, pos[0] * self.cell_w + 50 + self.cell_w // 2, pos[1] * self.cell_h + 50 + self.cell_h // 2)

            font_url = "./Assets/Poppins.ttf"
            font = pygame.font.Font(font_url, 30)
            t1 = Text(self.current_action, font, Color.WHITE)
            t1.show(self.screen, 1200, 80)
            t2 = Text(f"Score: {self.score}", font, Color.WHITE)
            t2.show(self.screen, 1200, 150)
            t3 = Text(f"HP: {self.HP}", font, Color.WHITE)
            t3.show(self.screen, 1200, 220)
            t3 = Text(f"Potion: {self.potion}", font, Color.WHITE)
            t3.show(self.screen, 1200, 290)

            if self.state < len(self.actions) - 1:
                self.update_state()
                sleep(0.2)
            elif self.state == len(self.actions) - 1:
                self.draw_agent(0, self.cell_h * len(self.cell_matrix))
                self.state += 1
            elif self.state == len(self.actions):
                print("Climb")
                self.robot[0].show(self.screen, 50, self.cell_h * (len(self.cell_matrix) + 1))

            pygame.display.update()
