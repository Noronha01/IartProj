# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
import copy
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, size):
        self.size = size
        self.grid = np.full((size, size), None, dtype=object)
        self.ships = np.array([4, 3, 2, 1])
        self.hints = []
        self.hints_dealt = []
        self.empty_cells = np.array([size*size])

    def set_values(self, row_values, col_values):
        self.row_values = row_values
        self.col_values = col_values

    def set_cell(self, row, col, value):
        if row >= 0 and row < self.size and col >= 0 and col < self.size and \
        self.get_value(row, col) == None:
            self.empty_cells -= 1
            if value.upper() != "W":
                self.grid[row][col] = value
                self.row_values[row] -= 1
                self.col_values[col] -= 1

                if self.row_values[row] == 0:
                    self.set_row_cells(row, "w")
                if self.col_values[col] == 0:
                    self.set_col_cells(col, "w")

                self.set_cell(row-1, col-1, "w")
                self.set_cell(row-1, col+1, "w")
                self.set_cell(row+1, col-1, "w")
                self.set_cell(row+1, col+1, "w")

                if value.upper() == "T":
                    self.set_cell(row-1, col, "w")
                    self.set_cell(row, col-1, "w")
                    self.set_cell(row, col+1, "w")

                elif value.upper() == "B":
                    self.set_cell(row+1, col, "w")
                    self.set_cell(row, col-1, "w")
                    self.set_cell(row, col+1, "w")

                elif value.upper() == "L":
                    self.set_cell(row, col-1, "w")
                    self.set_cell(row-1, col, "w")
                    self.set_cell(row+1, col, "w")

                elif value.upper() == "R":
                    self.set_cell(row, col+1, "w")
                    self.set_cell(row-1, col, "w")
                    self.set_cell(row+1, col, "w")

                elif value.upper() == "C":
                    self.set_cell(row, col+1, "w") 
                    self.set_cell(row-1, col, "w")
                    self.set_cell(row+1, col, "w")
                    self.set_cell(row, col-1, "w") 

            elif value.upper() == "W": 
                self.grid[row][col] = value                   


    def set_row_cells(self, row, value):
        for i in range(self.size):
            self.set_cell(row, i, value)

    def set_col_cells(self, col, value):
        for i in range(self.size):
            self.set_cell(i, col, value)

    def check_col_row_values(self):
        for i in range(self.size):
            if self.row_values[i] == 0:
                self.set_row_cells(i, "w")
            if self.col_values[i] == 0:
                self.set_col_cells(i, "w")

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return None
        value = self.grid[row][col]
        return value

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        # TODO
        pass

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        # TODO
        pass


    def find_mandatory_ships(self):

        for z in range(len(self.hints_dealt)):
            row, col = self.hints_dealt[z][0], self.hints_dealt[z][1]
            value = self.hints_dealt[z][2]


            if value == "T":

                if ((self.get_value(row+2, col) != None and self.get_value(row+2, col).upper() == "W") \
                or row+2 == self.size or self.col_values[col] == 1) and self.get_value(row+1, col) == None:
                    self.set_cell(row+1, col, "b")
                    self.hints_dealt[z][3] = 0
                    self.ships[1] -= 1
                else:
                    for i in range(1, 4):
                        if self.get_value(row+i, col) == "B":
                            for j in range(1, i):
                                self.set_cell(row+j, col, "m")
                            self.hints_dealt[z][3] = 0
                            self.ships[i] -= 1
                            break
                        elif self.get_value(row+i, col) != None:
                            break


            if value == "B":
                if ((self.get_value(row-2, col) != None and self.get_value(row-2, col).upper() == "W") or \
                row-1 == 0 or self.col_values[col] == 1) and self.get_value(row-1, col) == None:
                    self.set_cell(row-1, col, "t")
                    self.hints_dealt[z][3] = 0
                    self.ships[1] -= 1

                for i in range(1, 4):
                    if self.get_value(row-i, col) == "T":
                        self.hints_dealt[z][3] = 0
                        break


            elif value == "L":

                if ((self.get_value(row, col+2) != None and self.get_value(row, col+2).upper() == "W") or\
                col+2 == self.size-1 or self.row_values[row] == 1) and self.get_value(row, col+1) == None:
                    self.set_cell(row, col+1, "r")
                    self.hints_dealt[z][3] = 0
                    self.ships[1] -= 1
                else:
                    for i in range(1, 4):
                        if self.get_value(row, col+i) == "R":
                            for j in range(1, i):
                                self.set_cell(row, col+j, "m")
                            self.hints_dealt[z][3] = 0
                            self.ships[i] -= 1
                            break
                        elif self.get_value(row, col+i) != None:
                            break

            elif value == "R":
                if ((self.get_value(row, col-2) != None and self.get_value(row, col-2).upper() == "W") or\
                col-1 == 0 or self.row_values[row] == 1) and self.get_value(row, col-1) == None:
                    self.set_cell(row, col-1, "l")
                    self.hints_dealt[z][3] = 0
                    self.ships[1] -= 1

                for i in range(1, 4):
                    if self.get_value(row, col-i) == "L":
                        self.hints_dealt[z][3] = 0
                        break



    def cell_fits(self, row, col, hint):

        if self.get_value(row, col) != None or row < 0 or row >= self.size or col < 0 or col >= self.size or \
        self.row_values[row] <= 0 or self.col_values[col] <= 0:
                return False

        if hint == None:

            row1 = row-1
            col1 = col-1
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.get_value(row1+i, col1+j) != None and \
                    self.get_value(row1+i, col1+j).upper() != "W" and (row1+i != row and col1+i != col):
                        return False
                if self.get_value(row-2, col1+i) != None and self.get_value(row-2, col1+i).upper() == "T" or \
                self.get_value(row+2, col1+i) != None and self.get_value(row+2, col1+i).upper() == "B" or \
                self.get_value(row1+i, col-2) != None and self.get_value(row1+i, col-2).upper() == "L" or \
                self.get_value(row1+i, col+2) != None and self.get_value(row1+i, col+2).upper() == "R" or \
                self.get_value(row-1, col1+i) != None and self.get_value(row-1, col1+i).upper() == "T" or \
                self.get_value(row+1, col1+i) != None and self.get_value(row+1, col1+i).upper() == "B" or \
                self.get_value(row1+i, col-1) != None and self.get_value(row1+i, col-1).upper() == "L" or \
                self.get_value(row1+i, col+1) != None and self.get_value(row1+i, col+1).upper() == "R":
                    return False

        elif hint == "T":
            row1 = row-1
            col1 = col-1
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.get_value(row1+i, col1+j) != None and \
                    self.get_value(row1+i, col1+j).upper() != "W" and \
                    self.get_value(row1+i, col1+j) != "T" and (row1+i != row and col1+i != col):
                        return False
                if self.get_value(row+2, col1+i) != None and self.get_value(row+2, col1+i).upper() == "B" or \
                self.get_value(row1+i, col-2) != None and self.get_value(row1+i, col-2).upper() == "L" or \
                self.get_value(row1+i, col+2) != None and self.get_value(row1+i, col+2).upper() == "R":
                    return False


        elif hint == "B":

            row1 = row-1
            col1 = col-1
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.get_value(row1+i, col1+j) != None and \
                    self.get_value(row1+i, col1+j).upper() != "W" and \
                    self.get_value(row1+i, col1+j) != "B" and (row1+i != row and col1+i != col):
                        return False
                if self.get_value(row-2, col1+i) != None and self.get_value(row-2, col1+i).upper() == "T" or \
                self.get_value(row1+i, col-2) != None and self.get_value(row1+i, col-2).upper() == "L" or \
                self.get_value(row1+i, col+2) != None and self.get_value(row1+i, col+2).upper() == "R":
                    return False



        elif hint == "L":

            row1 = row-1
            col1 = col-1
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.get_value(row1+i, col1+j) != None and \
                    self.get_value(row1+i, col1+j).upper() != "W" and \
                    self.get_value(row1+i, col1+j) != "L" and (row1+i != row and col1+i != col):
                        return False
                if self.get_value(row-2, col1+i) != None and self.get_value(row-2, col1+i).upper() == "T" or \
                self.get_value(row+2, col1+i) != None and self.get_value(row+2, col1+i).upper() == "B" or \
                self.get_value(row1+i, col+2) != None and self.get_value(row1+i, col+2).upper() == "R":
                    return False

        elif hint == "R":

            row1 = row-1
            col1 = col-1
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.get_value(row1+i, col1+j) != None and \
                    self.get_value(row1+i, col1+j).upper() != "W" and \
                    self.get_value(row1+i, col1+j) != "R" and (row1+i != row and col1+i != col):
                        return False
                if self.get_value(row-2, col1+i) != None and self.get_value(row-2, col1+i).upper() == "T" or \
                self.get_value(row+2, col1+i) != None and self.get_value(row+2, col1+i).upper() == "B" or \
                self.get_value(row1+i, col-2) != None and self.get_value(row1+i, col-2).upper() == "L":
                    return False


        return True


    def ship_fits(self, row, col, size, orientation, hint):

        if self.ships[size-1] == 0:
            return False

        if hint == None:
            if orientation == "H":
                for i in range(size):
                    if not self.cell_fits(row, col+i, hint):
                        return False
            elif orientation == "V":
                for i in range(size):
                    if not self.cell_fits(row+i, col, hint):
                        return False
            elif orientation == "C" and not self.cell_fits(row, col, hint):
                return False

        elif hint == "T":
            for i in range(1, size):
                if not self.cell_fits(row+i, col, hint):
                    return False
        
        elif hint == "B":
            for i in range(1, size):
                if not self.cell_fits(row-i, col, hint):
                    return False

        elif hint == "L":
            for i in range(1, size):
                if not self.cell_fits(row, col+i, hint):
                    return False

        elif hint == "R":
            for i in range(1, size):
                if not self.cell_fits(row, col-i, hint):
                    return False

        return True




    def get_ships_from_pos(self):
        ships = np.empty((0, 5), dtype=object)

        count = 0
        for hint in self.hints_dealt:
            if hint[3] == 1:
                row, col = hint[0], hint[1]
                value = self.get_value(hint[0], hint[1])

                if value == "T" or value == "B":
                    for i in range(1, min(self.col_values[col]+1, 4)):
                        if self.ship_fits(row, col, i+1, "V", value):
                            if value == "B":
                                ship = np.array([(row-i, col, i+1, "V", value)], dtype=object)
                            else:
                                ship = np.array([(row, col, i+1, "V", value)], dtype=object)
                            ships = np.append(ships, ship, axis=0)

                elif value == "L" or value == "R":
                    for i in range(1, min(self.row_values[row]+1, 4)):
                        if self.ship_fits(row, col, i+1, "H", value):
                            if value == "R":
                                ship = np.array([(row, col-i, i+1, "H", value)], dtype=object)
                            else:
                                ship = np.array([(row, col, i+1, "H", value)], dtype=object)
                            ships = np.append(ships, ship, axis=0)

                count += 1

        if count == 0:
            for ship_size in range(3, -1, -1):
                if self.ships[ship_size] != 0:
                    break
            ship_size += 1

            row, col = np.where(self.grid == None)
            for row, col in zip(row, col):
                if ship_size == 1:
                    if self.ship_fits(row, col, 1, "C", None):
                        ship = np.array([(row, col, 1, "C", None)], dtype=object)
                        ships = np.append(ships, ship, axis=0)

                for i in range(1, min(self.row_values[row], 4)):
                    if ship_size == i+1 and self.ship_fits(row, col, i+1, "H", None):
                        ship = np.array([(row, col, i+1, "H", None)], dtype=object)
                        ships = np.append(ships, ship, axis=0)

                for i in range(1, min(self.col_values[col], 4)):
                    if ship_size == i+1 and self.ship_fits(row, col, i+1, "V", None):
                        ship = np.array([(row, col, i+1, "V", None)], dtype=object)
                        ships = np.append(ships, ship, axis=0)

        return ships


    def legal_board(self):

        for i in range(self.size):
            if self.row_values[i] > 0:
                count = 0
                for j in range(self.size):
                    if self.get_value(i, j) == None:
                        count += 1
                if count < self.row_values[i]:
                    return False
            if self.col_values[i] > 0:
                count1 = 0
                for w in range(self.size):
                    if self.get_value(w, i) == None:
                        count1 += 1
                if count1 < self.col_values[i]:
                    return False

        return True


    def print_board(self):
        for row in self.grid:
            for cell in row:
                if cell == "w" or cell is None:
                    print(".", end="")
                else:
                    print(cell, end="")
            print()

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board. """

        input_lines = sys.stdin.readlines()
        input_lines = [line.strip() for line in input_lines]

        row_values = list(map(int, input_lines[0].split()[1:]))
        col_values = list(map(int, input_lines[1].split()[1:]))


        board_size = len(row_values)
        board = Board(board_size)

        board.set_values(row_values, col_values)


        hint_lines = input_lines[3:]  # Skip the first three lines

        for line in hint_lines:
            _, row, col, hint_value = line.split()
            if hint_value != "M":
                row = int(row)
                col = int(col)
                board.set_cell(row, col, hint_value)

                if hint_value != "W" and hint_value != "C":
                    board.hints_dealt.append([row, col, hint_value, 1])

                if hint_value == "C":
                    board.ships[0] -= 1

                if hint_value == "W":
                    board.hints.append((row, col, hint_value))
            else:
                board.hints.append((row, col, hint_value))

        board.check_col_row_values()
        board.find_mandatory_ships()


        return board


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        
        super().__init__(BimaruState(board))

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        if not state.board.legal_board():
            return []

        actions = state.board.get_ships_from_pos()

        size = len(actions)

        if size > 0:
            if actions[0][4] == None and size < state.board.ships[actions[0][2]-1]:
                return []

        #sorted_actions = sorted(actions, key=lambda x: x[2], reverse=True)
        #print(actions)
        #return sorted_actions
        return actions

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        new_board = Board(state.board.size)
        new_board.grid = copy.deepcopy(state.board.grid)
        new_board.size = copy.deepcopy(state.board.size)
        new_board.hints = copy.deepcopy(state.board.hints)
        new_board.row_values = copy.deepcopy(state.board.row_values)
        new_board.col_values = copy.deepcopy(state.board.col_values)
        new_board.ships = copy.deepcopy(state.board.ships)
        new_board.hints_dealt = copy.deepcopy(state.board.hints_dealt)
        new_board.empty_cells = copy.deepcopy(state.board.empty_cells)
        new_state = BimaruState(new_board)

        row = action[0]
        col = action[1]
        size = action[2]
        orientation = action[3]
        hint = action[4]


        if orientation == "C":
            new_state.board.set_cell(row, col, "c")

        elif orientation == "H":
            new_state.board.set_cell(row, col, "l")

            for i in range(1, size-1):
                new_state.board.set_cell(row, col+i, "m")

            new_state.board.set_cell(row, col+size-1, "r")

        elif orientation == "V":
            new_state.board.set_cell(row, col, "t")

            for i in range(1, size-1):
                new_state.board.set_cell(row+i, col, "m")

            new_state.board.set_cell(row+size-1, col, "b")

        if hint != None:
            if hint == "T" or hint == "L":
                for h in range(len(new_state.board.hints_dealt)):
                    if row == new_state.board.hints_dealt[h][0] and \
                    col == new_state.board.hints_dealt[h][1] and hint == new_state.board.hints_dealt[h][2]:
                        new_state.board.hints_dealt[h][3] = 0
            elif hint == "B":
                for h in range(len(new_state.board.hints_dealt)):
                    if row+size-1 == new_state.board.hints_dealt[h][0] and \
                    col == new_state.board.hints_dealt[h][1] and hint == new_state.board.hints_dealt[h][2]:
                        new_state.board.hints_dealt[h][3] = 0
            elif hint == "R":
                for h in range(len(new_state.board.hints_dealt)):
                    if col+size-1 == new_state.board.hints_dealt[h][1] and \
                    row == new_state.board.hints_dealt[h][0] and hint == new_state.board.hints_dealt[h][2]:
                        new_state.board.hints_dealt[h][3] = 0


        new_state.board.ships[size-1] -= 1


        return new_state

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        
        for i in range(state.board.size):
            if state.board.row_values[i] > 0 or state.board.col_values[i] > 0:
                return False

        for ship in state.board.ships:
            if ship > 0:
                return False

        
        for hint in state.board.hints:
            if (state.board.get_value(int(hint[0]), int(hint[1])) != None and \
            state.board.get_value(int(hint[0]), int(hint[1])).upper() != hint[2]) or \
            state.board.get_value(int(hint[0]), int(hint[1])) == None:
                return False

            else:
                if hint[2] == "M":
                    state.board.grid[int(hint[0])][int(hint[1])] = "M"
                elif hint[2] == "W":
                    state.board.grid[int(hint[0])][int(hint[1])] = "W"


        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # Calculate the number of remaining ships to be placed

        """
        remaining_ships = sum(node.state.board.ships)
        count = 0

        for value in range(node.state.board.size):
            if node.state.board.row_values[value] > 0:
                count += 1
            if node.state.board.col_values[value] > 0:
                count += 1

        # Calculate the total number of cells with unknown content
        unknown_cells = np.count_nonzero(node.state.board.grid == None)

        # Estimate the minimum number of moves required
        min_moves = 100*remaining_ships + count + unknown_cells

        return min_moves

        """


"""
def main():
    board = Board.parse_instance()
    bimaru = Bimaru(board)
    solution = depth_first_tree_search(bimaru)
    solution.state.board.print_board()
"""

if __name__ == "__main__":
    board = Board.parse_instance()
    bimaru = Bimaru(board)
    solution = depth_first_tree_search(bimaru)
    #solution = astar_search(bimaru)
    #solution = breadth_first_tree_search(bimaru)
    solution.state.board.print_board()
    #cProfile.run("main()")

