import Program
from enum import Enum
from Cell import Cell, Object
from KnowledgeBase import KnowledgeBase
import copy
from Program import Program
class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
class Action(Enum):
    TURN_LEFT = 1
    TURN_RIGHT = 2
    MOVE_FORWARD = 3
    GRAB_GOLD = 4
    GRAB_POTION = 5
    SHOOT = 6
    HEAL = 7
    CLIMB = 8

class Agent:
    def __init__(self, program: Program, output_filename: str):
        self.program = program
        self.output_filename = output_filename

        self.map_size = None
        self.cell_matrix = None
        self.init_cell_matrix = copy.deepcopy(self.program.cell_matrix)

        self.cave_cell = Cell((-1, -1), 10, Object.EMPTY.value)
        self.agent_cell = Cell((9, 0), 10, Object.EMPTY.value)
        self.agent_cell.update_parent(self.cave_cell)
        self.init_agent_cell = Cell((9, 0), 10, Object.EMPTY.value)
        self.cell_matrix = program.cell_matrix
        self.KB = KnowledgeBase()
        self.path = []
        self.action_list = []
        self.score = 0
        self.direction = Direction.UP
        self.HP = 100
        self.potion = 0

    def append_event_to_output_file(self, text: str):
        out_file = open(self.output_filename, 'a')
        out_file.write(text + '\n')
        out_file.close()

    def add_action(self, action):
        self.action_list.append(action)
        self.append_event_to_output_file(action.name)

        if action == Action.TURN_LEFT:
            pass
        elif action == Action.TURN_RIGHT:
            pass
        elif action == Action.MOVE_FORWARD:
            self.score -= 10
            self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.GRAB_GOLD:
            self.score += 5000
            self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.GRAB_POTION:
            self.score -= 10
            self.potion += 1
            self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.SHOOT:
            self.score -= 100
            self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.CLIMB:
            self.score += 10
            self.append_event_to_output_file('Score: ' + str(self.score))
        elif action == Action.HEAL:
            self.score -= 10
            self.HP = min(100, self.HP + 25)
            self.potion -= 1
            self.append_event_to_output_file('Score: ' + str(self.score))
        else:
            raise TypeError("Error: " + self.add_action.__name__)

    def add_new_percepts_to_KB(self, cell):
        adj_cell_list = cell.get_adj_cell_list(self.cell_matrix)

        sign = '-'
        if cell.exist_pit():
            sign = '+'
        self.KB.add_clause([cell.get_literal(Object.PIT, sign)])

        # PL: Wumpus?
        sign = '-'
        if cell.exist_wumpus():
            sign = '+'
        self.KB.add_clause([cell.get_literal(Object.WUMPUS, sign)])

        # PL: Poisonous Gas?
        sign = '-'
        if cell.exist_poisonousgas():
            sign = '+'
        self.KB.add_clause([cell.get_literal(Object.POISONOUSGAS, sign)])

        # PL: Breeze?
        sign = '-'
        if cell.exist_breeze():
            sign = '+'
        self.KB.add_clause([cell.get_literal(Object.BREEZE, sign)])

        # PL: Stench?
        sign = '-'
        if cell.exist_stench():
            sign = '+'
        self.KB.add_clause([cell.get_literal(Object.STENCH, sign)])

        #PL: Whiff
        sign = '-'
        if cell.exist_whiff():
            sign = '+'
        self.KB.add_clause([cell.get_literal(Object.WHIFF, sign)])

        #PL: Glow
        sign = '-'
        if cell.exist_glow():
            sign = '+'
        self.KB.add_clause([cell.get_literal(Object.GLOW, sign)])

        # PL: This cell has Breeze iff At least one of all of adjacent cells has a Pit.
        # B <=> Pa v Pb v Pc v Pd
        if cell.exist_breeze():
            # B => Pa v Pb v Pc v Pd
            clause = [cell.get_literal(Object.BREEZE, '-')]
            for adj_cell in adj_cell_list:
                clause.append(adj_cell.get_literal(Object.PIT, '+'))
            self.KB.add_clause(clause)

            # Pa v Pb v Pc v Pd => B
            # ~(Pa v Pb v Pc v Pd) v B
            # (~Pa ^ ~Pb ^ ~Pc ^ ~Pd) v B

            for adj_cell in adj_cell_list:
                clause = [cell.get_literal(Object.BREEZE, '+'),
                          adj_cell.get_literal(Object.PIT, '-')]
                self.KB.add_clause(clause)

        # PL: This cell has no Breeze then all of adjacent cells has no Pit.
        # -Pa ^ -Pb ^ -Pc ^ -Pd
        else:
            for adj_cell in adj_cell_list:
                clause = [adj_cell.get_literal(Object.PIT, '-')]
                self.KB.add_clause(clause)

        # PL: This cell has Stench iff At least one of all of adjacent cells has a Wumpus.


        if cell.exist_stench():
            # S => Wa v Wb v Wc v Wd
            clause = [cell.get_literal(Object.STENCH, '-')]
            for adj_cell in adj_cell_list:
                clause.append(adj_cell.get_literal(Object.WUMPUS, '+'))
            self.KB.add_clause(clause)

            # Wa v Wb v Wc v Wd => S
            for adj_cell in adj_cell_list:
                clause = [cell.get_literal(Object.STENCH, '+'),
                          adj_cell.get_literal(Object.WUMPUS, '-')]
                self.KB.add_clause(clause)

        # PL: This cell has no Stench then all of adjacent cells has no Wumpus.
        # -Wa ^ -Wb ^ -Wc ^ -Wd
        else:
            for adj_cell in adj_cell_list:
                clause = [adj_cell.get_literal(Object.WUMPUS, '-')]
                self.KB.add_clause(clause)

        if cell.exist_whiff():
            # Wh => PGa v PGb v PGc v PGd
            clause = [cell.get_literal(Object.WHIFF, '-')]
            for adj_cell in adj_cell_list:
                clause.append(adj_cell.get_literal(Object.POISONOUSGAS, '+'))
            self.KB.add_clause(clause)

            # PGa v PGb v PGc v PGd => Wh
            for adj_cell in adj_cell_list:
                clause = [cell.get_literal(Object.WHIFF, '+'),
                          adj_cell.get_literal(Object.POISONOUSGAS, '-')]
                self.KB.add_clause(clause)

        # PL: This cell has no Whiff then all of adjacent cells has no Poisonous Gas.
        # -PGa ^ -PGb ^ -PGc ^ -PGd
        else:
            for adj_cell in adj_cell_list:
                clause = [adj_cell.get_literal(Object.POISONOUSGAS, '-')]
                self.KB.add_clause(clause)

        if cell.exist_glow():
            # GL => HPa v HPb v HPc v HPd
            clause = [cell.get_literal(Object.GLOW, '-')]
            for adj_cell in adj_cell_list:
                clause.append(adj_cell.get_literal(Object.HEALINGPOTION, '+'))
            self.KB.add_clause(clause)

            # HPa v HPb v HPc v HPd => GL
            for adj_cell in adj_cell_list:
                clause = [cell.get_literal(Object.GLOW, '+'),
                          adj_cell.get_literal(Object.HEALINGPOTION, '-')]
                self.KB.add_clause(clause)

        # PL: This cell has no Stench then all of adjacent cells has no Wumpus.
        # -HPa ^ -HPb ^ -HPc ^ -HPd
        else:
            for adj_cell in adj_cell_list:
                clause = [adj_cell.get_literal(Object.HEALINGPOTION, '-')]
                self.KB.add_clause(clause)
        self.append_event_to_output_file(str(self.KB.KB))

    def turn_to(self, next_cell):
        if next_cell.map_pos[0] == self.agent_cell.map_pos[0]:
            if next_cell.map_pos[1] - self.agent_cell.map_pos[1] == 1:
                if self.direction == Direction.UP:
                    pass
                elif self.direction == Direction.DOWN:
                    self.add_action(Action.TURN_RIGHT)
                    self.add_action(Action.TURN_RIGHT)
                elif self.direction == Direction.LEFT:
                    self.add_action(Action.TURN_RIGHT)
                else:
                    self.add_action(Action.TURN_LEFT)
                self.direction = Direction.UP
            else:
                if self.direction == Direction.UP:
                    self.add_action(Action.TURN_RIGHT)
                    self.add_action(Action.TURN_RIGHT)
                elif self.direction == Direction.DOWN:
                    pass
                elif self.direction == Direction.LEFT:
                    self.add_action(Action.TURN_LEFT)
                else:
                    self.add_action(Action.TURN_RIGHT)
                self.direction = Direction.DOWN
        elif next_cell.map_pos[1] == self.agent_cell.map_pos[1]:
            if next_cell.map_pos[0] - self.agent_cell.map_pos[0] == 1:
                if self.direction == Direction.UP:
                    self.add_action(Action.TURN_RIGHT)
                elif self.direction == Direction.DOWN:
                    self.add_action(Action.TURN_LEFT)
                elif self.direction == Direction.LEFT:
                    self.add_action(Action.TURN_RIGHT)
                    self.add_action(Action.TURN_RIGHT)
                else:
                    pass
                self.direction = Direction.RIGHT
            else:
                if self.direction == Direction.UP:
                    self.add_action(Action.TURN_LEFT)
                elif self.direction == Direction.DOWN:
                    self.add_action(Action.TURN_RIGHT)
                elif self.direction == Direction.LEFT:
                    pass
                else:
                    self.add_action(Action.TURN_RIGHT)
                    self.add_action(Action.TURN_RIGHT)
                self.direction = Direction.LEFT
        else:
            raise TypeError('Error: ' + self.turn_to.__name__)

    def move_to(self, next_cell):
        self.turn_to(next_cell)
        self.add_action(Action.MOVE_FORWARD)
        self.agent_cell = next_cell

    def backtracking_search(self):
        # If there is a Pit, Agent dies.
        if self.agent_cell.exist_pit():
            self.score -= 10000
            return False

        # If there is a Wumpus, Agent dies.
        if self.agent_cell.exist_wumpus():
            self.score -= 10000
            return False
        if self.agent_cell.exist_poisonousgas():
            self.HP -= 25
            if self.HP <= 0:
                return False
        if self.HP < 100 and self.potion > 0:
            self.add_action(Action.HEAL)

        # If there is Gold, Agent grabs Gold.
        if self.agent_cell.exist_gold():
            self.add_action(Action.GRAB_GOLD)
            self.agent_cell.grab_gold()

        if self.agent_cell.exist_healingpotion():
            self.add_action(Action.GRAB_POTION)
            self.agent_cell.grab_heal(self.KB, self.cell_matrix)

        # If this cell is not explored, mark this cell as explored then add new percepts to the KB.
        if not self.agent_cell.is_explored():
            self.agent_cell.explore()
            self.add_new_percepts_to_KB(self.agent_cell)

        # Initialize valid_adj_cell_list.
        valid_adj_cell_list = self.agent_cell.get_adj_cell_list(self.cell_matrix)

        # Discard the parent_cell from the valid_adj_cell_list.
        temp_adj_cell_list = []
        if self.agent_cell.parent in valid_adj_cell_list:
            valid_adj_cell_list.remove(self.agent_cell.parent)

        # Store previos agent's cell.
        pre_agent_cell = self.agent_cell

        # If the current cell is OK (there is no Breeze or Stench), Agent move to all of valid adjacent cells.
        # If the current cell has Breeze or/and Stench, Agent infers base on the KB to make a decision.
        if not self.agent_cell.is_OK():
            # Discard all of explored cells having Pit from the valid_adj_cell_list.
            temp_adj_cell_list = []
            for valid_adj_cell in valid_adj_cell_list:
                if valid_adj_cell.is_explored() and valid_adj_cell.exist_pit():
                    temp_adj_cell_list.append(valid_adj_cell)
            for adj_cell in temp_adj_cell_list:
                valid_adj_cell_list.remove(adj_cell)

            temp_adj_cell_list = []

            # If the current cell has Stench, Agent infers whether the valid adjacent cells have Wumpus.
            if self.agent_cell.exist_stench():
                valid_adj_cell: Cell
                for valid_adj_cell in valid_adj_cell_list:
                    self.append_event_to_output_file('Infer: ' + str(valid_adj_cell.map_pos))

                    # Infer Wumpus.
                    not_alpha = [[valid_adj_cell.get_literal(Object.WUMPUS, '-')]]
                    have_wumpus = self.KB.infer(not_alpha)

                    # If we can infer Wumpus.
                    if have_wumpus:
                        # Dectect Wumpus.

                        # Shoot this Wumpus.
                        self.add_action(Action.SHOOT)
                        valid_adj_cell.kill_wumpus(self.cell_matrix, self.KB)
                        self.append_event_to_output_file('KB: ' + str(self.KB.KB))

                    # If we can not infer Wumpus.
                    else:
                        # Infer not Wumpus.
                        not_alpha = [[valid_adj_cell.get_literal(Object.WUMPUS, '+')]]
                        have_no_wumpus = self.KB.infer(not_alpha)

                        # If we can infer not Wumpus.
                        if have_no_wumpus:
                            # Detect no Wumpus.
                            pass

                        # If we can not infer not Wumpus.
                        else:
                            # Discard these cells from the valid_adj_cell_list.
                            if valid_adj_cell not in temp_adj_cell_list:
                                temp_adj_cell_list.append(valid_adj_cell)
            if self.agent_cell.exist_stench():
                adj_cell_list = self.agent_cell.get_adj_cell_list(self.cell_matrix)
                if self.agent_cell.parent in adj_cell_list:
                    adj_cell_list.remove(self.agent_cell.parent)

                explored_cell_list = []
                for adj_cell in adj_cell_list:
                    if adj_cell.is_explored():
                        explored_cell_list.append(adj_cell)
                for explored_cell in explored_cell_list:
                    adj_cell_list.remove(explored_cell)

                for adj_cell in adj_cell_list:
                    self.append_event_to_output_file('Try: ' + str(adj_cell.map_pos))
                    self.turn_to(adj_cell)

                    self.add_action(Action.SHOOT)
                    if adj_cell.exist_wumpus():
                        adj_cell.kill_wumpus(self.cell_matrix, self.KB)
                        self.append_event_to_output_file('KB: ' + str(self.KB.KB))

                    if not self.agent_cell.exist_stench():
                        self.agent_cell.update_child_list([adj_cell])
                        break
            # If the current cell has Breeze, Agent infers whether the adjacent cells have Pit.
            if self.agent_cell.exist_breeze():
                valid_adj_cell: Cell
                for valid_adj_cell in valid_adj_cell_list:
                    self.append_event_to_output_file('Infer: ' + str(valid_adj_cell.map_pos))

                    # Infer Pit.
                    not_alpha = [[valid_adj_cell.get_literal(Object.PIT, '-')]]
                    have_pit = self.KB.infer(not_alpha)

                    # If we can infer Pit.
                    if have_pit:
                        # Detect Pit.

                        # Mark these cells as explored.
                        valid_adj_cell.explore()

                        # Add new percepts of these cells to the KB.
                        self.KB.add_clause([valid_adj_cell.get_literal(Object.PIT, "+")])

                        # Update parent for this cell.
                        valid_adj_cell.update_parent(valid_adj_cell)

                        # Discard these cells from the valid_adj_cell_list.
                        temp_adj_cell_list.append(valid_adj_cell)

                    # If we can not infer Pit.
                    else:
                        # Infer not Pit.
                        not_alpha = [[valid_adj_cell.get_literal(Object.PIT, '+')]]
                        have_no_pit = self.KB.infer(not_alpha)

                        # If we can infer not Pit.
                        if have_no_pit:
                            # Detect no Pit.
                            pass

                        # If we can not infer not Pit.
                        else:
                            # Discard these cells from the valid_adj_cell_list.
                            temp_adj_cell_list.append(valid_adj_cell)

            if self.agent_cell.exist_whiff():
                valid_adj_cell: Cell
                for valid_adj_cell in valid_adj_cell_list:
                    self.append_event_to_output_file('Infer: ' + str(valid_adj_cell.map_pos))

                    # Infer Poisonous Gas.
                    not_alpha = [[valid_adj_cell.get_literal(Object.POISONOUSGAS, '-')]]
                    have_pg = self.KB.infer(not_alpha)

                    # If we can infer Poisonous Gas.
                    if have_pg:
                        # Detect Poisonous Gas.

                        # Mark these cells as explored.
                        valid_adj_cell.explore()

                        # Add new percepts of these cells to the KB.
                        self.KB.add_clause([valid_adj_cell.get_literal(Object.POISONOUSGAS, "+")])

                        # Update parent for this cell.
                        valid_adj_cell.update_parent(valid_adj_cell)

                        # Discard these cells from the valid_adj_cell_list.
                        if self.HP <= 50:
                            temp_adj_cell_list.append(valid_adj_cell)

                    # If we can not infer Poisonous Gas.
                    else:
                        # Infer not Poisonous Gas.
                        not_alpha = [[valid_adj_cell.get_literal(Object.POISONOUSGAS, '+')]]
                        have_no_pg = self.KB.infer(not_alpha)

                        # If we can infer not Poisonous Gas.
                        if have_no_pg:
                            # Detect no Poisonous Gas.
                            pass

                        # If we can not infer not Poisonous Gas.
                        else:
                            # Discard these cells from the valid_adj_cell_list.
                            if self.HP <= 50:
                                temp_adj_cell_list.append(valid_adj_cell)

        temp_adj_cell_list = list(set(temp_adj_cell_list))

        # Select all of the valid nexts cell from the current cell.
        for adj_cell in temp_adj_cell_list:
            valid_adj_cell_list.remove(adj_cell)
        self.agent_cell.update_child_list(valid_adj_cell_list)

        # Move to all of the valid next cells sequentially.
        for next_cell in self.agent_cell.child_list:
            self.move_to(next_cell)
            self.append_event_to_output_file('Move to: ' + str(self.agent_cell.map_pos))

            if not self.backtracking_search():
                return False

            self.move_to(pre_agent_cell)
            self.append_event_to_output_file('Backtrack: ' + str(pre_agent_cell.map_pos))

        return True

    def solve_wumpus_world(self):
        # Reset file output
        out_file = open(self.output_filename, 'w')
        out_file.close()

        self.backtracking_search()

        # victory_flag = True
        # for cell_row in self.cell_matrix:
        #     for cell in cell_row:
        #         if cell.exist_gold() or cell.exist_wumpus():
        #             victory_flag = False
        #             break
        # if victory_flag:
        #     self.add_action(Action.KILL_ALL_WUMPUS_AND_GRAB_ALL_FOOD)

        if self.agent_cell.parent == self.cave_cell:
            self.add_action(Action.CLIMB)
        print("Score:", self.score)
        return self.action_list, self.init_cell_matrix

if __name__ == '__main__':
    program = Program("./map1.txt")
    agent = Agent(program, "out1.txt")
    agent.solve_wumpus_world()