from enum import Enum

class Object(Enum):
    GOLD   = 'G'
    PIT    = 'P'
    WUMPUS = 'W'
    BREEZE = 'B'
    STENCH = 'S'
    AGENT  = 'A'
    EMPTY  = '-'
    HEALINGPOTION = 'H_P'
    POISONOUSGAS = 'P_G'
    WHIFF = 'W_H'
    GLOW = 'G_L'


class Cell:
    def __init__(self, matrix_pos, map_size, objects_str):
        self.matrix_pos = matrix_pos                                            # (0, 0) (0, 1) ... (9, 9)   (TL -> BR)
        self.map_pos = matrix_pos[1] + 1, map_size - matrix_pos[0]              # (1, 1) (1, 2) ... (10, 10) (BL -> TR)
        self.index_pos = map_size * (self.map_pos[1] - 1) + self.map_pos[0]     # 1 2 3 ... 99 100           (BL -> TR)
        self.map_size = map_size

        self.explored = False
        self.percept = [False] * 9  # [-G, -P, -W, -B, -S,-H_P,-P_G,-W_H,-G_L]
        self.init(objects_str)

        self.parent = None
        self.child_list = []


    def init(self, objects_list_str):
        percept_mapping = {
            Object.GOLD.value: 0,
            Object.PIT.value: 1,
            Object.WUMPUS.value: 2,
            Object.BREEZE.value: 3,
            Object.STENCH.value: 4,
            Object.HEALINGPOTION.value: 5,
            Object.POISONOUSGAS.value: 6,
            Object.WHIFF.value: 7,
            Object.GLOW.value: 8
        }

        for obj in objects_list_str:
            if obj in percept_mapping:
                self.percept[percept_mapping[obj]] = True
            elif obj in {Object.AGENT.value, Object.EMPTY.value}:
                continue
            else:
                raise TypeError('Error: Cell.init')
    def get_literal(self, obj: Object, sign='+'):    # sign='-': not operator
        index_mapping = {
            Object.PIT: 1,
            Object.WUMPUS: 2,
            Object.BREEZE: 3,
            Object.STENCH: 4,
            Object.HEALINGPOTION: 5,
            Object.POISONOUSGAS: 6,
            Object.WHIFF: 7,
            Object.GLOW: 8
        }

        if obj not in index_mapping:
            raise ValueError('Error in MapCell.formulate_literal')

        factor = 10 ** len(str(self.map_size ** 2))
        literal = index_mapping[obj] * factor + self.index_pos
        return -literal if sign == '-' else literal       
    def exist_gold(self):
        return self.percept[0]

    def exist_pit(self):
        return self.percept[1]

    def exist_wumpus(self):
        return self.percept[2]

    def exist_breeze(self):
        return self.percept[3]

    def exist_stench(self):
        return self.percept[4]
    
    def exist_healingpotion(self):
        return self.percept[5]
    
    def exist_poisonousgas(self):
        return self.percept[6]
    
    def exist_whiff(self):
        return self.percept[7]
    
    def exist_glow(self):
        return self.percept[8]
    
    def is_OK(self):
         return not (self.exist_breeze() or self.exist_stench() or self.exist_whiff())
    
    def update_parent(self, parent_cell):
        self.parent = parent_cell

    def grab_gold(self):
        self.percept[0] = False
    def get_adj_cell_list(self, cell_matrix):
        adj_cell_list = []
        adj_cell_matrix_pos_list = [(self.matrix_pos[0], self.matrix_pos[1] + 1),   # Right
                                    (self.matrix_pos[0], self.matrix_pos[1] - 1),   # Left
                                    (self.matrix_pos[0] - 1, self.matrix_pos[1]),   # Up
                                    (self.matrix_pos[0] + 1, self.matrix_pos[1])]   # Down

        for adj_cell_matrix_pos in adj_cell_matrix_pos_list:
            if 0 <= adj_cell_matrix_pos[0] < self.map_size and 0 <= adj_cell_matrix_pos[1] < self.map_size:
                adj_cell_list.append(cell_matrix[adj_cell_matrix_pos[0]][adj_cell_matrix_pos[1]])

        return adj_cell_list
    #heal
    def grab_heal(self, kb, glow_cell, cell_matrix):
        #delete healing potion
        self.percept[5] = False

        #Get adjacent cells of the healing potion cell
        adj_cells = self.get_adj_cell_list(cell_matrix)

        for glow_cell in adj_cells:
            if not any(adj_cell.exist_healingpotion() for adj_cell in glow_cell.get_adj_cell_list(cell_matrix)):
                #Remove glow perception from the glow cell
                glow_cell.percept[8] = False
                self.update_kb_glow(kb, glow_cell, cell_matrix)
    

    def update_kb_glow(self, kb, glow_cell, cell_matrix):
        #Remove existing clause: glow at this cell
        literal = self.get_literal(Object.GLOW, '+')
        kb.del_clause([literal])

        #Add clause: No glow at this cell
        literal = self.get_literal(Object.GLOW, '-')
        kb.add_clause([literal])

        #Remove clauses related to glow propagation
        adj_cells = glow_cell.get_adj_cell_list(cell_matrix)
        kb.del_clause([glow_cell.get_literal(Object.GLOW, '-')])

        #Iterate through each adjacent cell to remove related clauses
        for adj_cell in adj_cells:
            #Remove clause: If healing potion exists in any adjacent cell, there should be a glow
            kb.del_clause([glow_cell.get_literal(Object.GLOW, '+'), adj_cell.get_literal(Object.HEALINGPOTION, '-')])


    def kill_wumpus(self, cell_matrix, kb):
        # Delete Wumpus.
        self.percept[2] = False

        # Get adjacent cells of the Wumpus cell.
        adj_cells = self.get_adj_cell_list(cell_matrix)

        for stench_cell in adj_cells:
            if not any(adj_cell.exist_wumpus() for adj_cell in stench_cell.get_adj_cell_list(cell_matrix)):
                # Remove stench perception from the stench cell.
                stench_cell.percept[4] = False
                self.update_kb_stench(kb, stench_cell, cell_matrix)

    def update_kb_stench(self, kb, stench_cell, cell_matrix):
        # Remove existing clause: Stench at this cell.
        literal = self.get_literal(Object.STENCH, '+')
        kb.del_clause([literal])

        # Add clause: No stench at this cell.
        literal = self.get_literal(Object.STENCH, '-')
        kb.add_clause([literal])

        # Remove clauses related to stench propagation.
        adj_cells = stench_cell.get_adj_cell_list(cell_matrix)
        kb.del_clause([stench_cell.get_literal(Object.STENCH, '-')])

        # Iterate through each adjacent cell to remove related clauses.
        for adj_cell in adj_cells:
            # Remove clause: If Wumpus exists in any adjacent cell, there should be a stench.
            kb.del_clause([stench_cell.get_literal(Object.STENCH, '+'), adj_cell.get_literal(Object.WUMPUS, '-')])

    


    def is_explored(self):
        return self.explored

    def explore(self):
        self.explored = True


    def update_child_list(self, valid_adj_cell_list):
        for adj_cell in valid_adj_cell_list:
            if adj_cell.parent is None:
                self.child_list.append(adj_cell)
                adj_cell.update_parent(self)


    
