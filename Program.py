import numpy as np 
from Cell import Cell
from enum import Enum
class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
class Program:
    def __init__(self, file_path):
        self.file_path = file_path
        self.map_matrix = self.read_map()
        self.update_percepts()
        self.cell_matrix = self.matrix_cells()
    def custom_split(self, line):
        elements = []
        current_element = ''
        for char in line:
            if char == '.':
                if current_element:
                    
                    elements.append(current_element)
                    current_element = '' 
            else:
                current_element += char
            
        if current_element:
            elements.append(current_element)
        return elements
    def read_map(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        
        
        N = int(lines[0].strip())
        
        
        map_matrix = [['-' for _ in range(N)] for _ in range(N)]
        
        
        for i in range(1, N+1):
            row = self.custom_split(lines[i].strip())
            map_matrix[i-1] = row
            
         
        return map_matrix
    def update_percepts(self):
        N = len(self.map_matrix)
        directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        
        for i in range(N):
            for j in range(N):
                result = []
                result.extend(self.map_matrix[i][j].split('/'))
                if  'W' in result:  # Wumpus
                    for direction in directions:
                        ni, nj = i + direction.value[0], j + direction.value[1]
                        if 0 <= ni < N and 0 <= nj < N:
                            if self.map_matrix[ni][nj] == '-':
                                self.map_matrix[ni][nj] = 'S'
                            elif 'S' not in self.map_matrix[ni][nj]:
                                self.map_matrix[ni][nj] += '/S' # Stench
                             
                if  'P' in result:  # Pit
                    for direction in directions:
                        ni, nj = i + direction.value[0], j + direction.value[1]
                        if 0 <= ni < N and 0 <= nj < N:
                            if self.map_matrix[ni][nj] == '-':
                                self.map_matrix[ni][nj] = 'B'
                            elif 'B' not in self.map_matrix[ni][nj]:
                                self.map_matrix[ni][nj] += '/B' # Breeze
                if  'P_G' in result :  # Poisonous Gas
                    for direction in directions:
                        ni, nj = i + direction.value[0], j + direction.value[1]
                        if 0 <= ni < N and 0 <= nj < N:
                            if self.map_matrix[ni][nj] == '-':
                                self.map_matrix[ni][nj] = 'W_H'
                            elif 'W_H' not in self.map_matrix[ni][nj]:
                                self.map_matrix[ni][nj] += '/W_H'   # Whiff
                if  'H_P' in result:  # Healing Potions
                    for direction in directions:
                        ni, nj = i + direction.value[0], j + direction.value[1]
                        if 0 <= ni < N and 0 <= nj < N:
                            if self.map_matrix[ni][nj] == '-':
                                self.map_matrix[ni][nj] = 'G_L'
                            elif 'G_L' not in self.map_matrix[ni][nj]:
                                self.map_matrix[ni][nj] += '/G_L'  # Glow
    
    def matrix_cells(self):
        N = len(self.map_matrix)
        matrix = [[Cell((i, j), N, self.map_matrix[i][j]) for j in range(N)] for i in range(N)]
        return matrix
    def display_map(self):
        
        for row in self.map_matrix:
            print(' '.join(row))

    # grab gold and Health Potion
    def grab(self, target_position):
        x, y = target_position
        if 'H' in self.map_matrix[x][y]:
            self.map_matrix[x][y] = self.map_matrix[x][y].replace('H', '-')
            return "HP grabbed"
        elif 'G' in self.map_matrix[x][y]:
            self.map_matrix[x][y] = self.map_matrix[x][y].replace('G', '-')
            return "Gold grabbed"
        return "No gold or HP here"
    # info about the cell in front of the agent
    def info_forward(self, target_position):
        x, y = target_position
        return self.map_matrix[x][y]
    
    # shoot at the target position
    def shoot(self, target_position):
        x, y = target_position
        if 'W' in self.map_matrix[x][y]:  
            self.map_matrix[x][y] = self.map_matrix[x][y].replace('W', '-')
            return "Hit"
        return "Miss"

    # action: forward, grab, shoot
    # target_position: (x, y)
    def actionResult(self, action, target_position=None):
        if action == 'forward':
            if target_position is None:
                return "Target position required for move forward"
            return self.info_forward(target_position)
        elif action == 'grab':
            return self.grab()
        elif action == 'shoot':
            if target_position is None:
                return "Target position required for shooting"
            return self.shoot(target_position)
        else:
            return "Invalid action"

                                            ##### TEST MAP #####
def test_read_map():
    program = Program('test1.txt')
    program.update_percepts()
    program.display_map()
    print('==========================')
    program.map_matrix = program.matrix_cells()
    map_matrix = program.map_matrix
    
    for row in map_matrix:
        for cell in row:
            assert isinstance(cell, Cell), f"Expected Cell, got {type(cell)}"
            print(f"Cell at {cell.matrix_pos} with type {cell.percept}")

# Run the test
# test_read_map()
