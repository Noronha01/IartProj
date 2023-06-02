# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 46:
# 102543 Pedro Noronha
# 00000 Mariana Carvalho

import sys
import copy
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
        self.grid = [[None] * size for _ in range(size)]
        self.ships = [4, 3, 2, 1]

    def set_cell(self, row, col, value):
        # check if it legal to set this cell
        if row >= 0 and row < self.size and col >= 0 and col < self.size and self.get_value(row, col) == None:
            self.grid[row][col] = value
            if value.upper() != "W":
                self.row_values[row] -= 1
                self.col_values[col] -= 1
                if self.row_values[row] == 0:
                    self.set_row_cells(row, "w")
                if self.col_values[col] == 0:
                    self.set_column_cells(col, "w")


    def set_row_cells(self, row, value):
        for i in range(self.size):
            self.set_cell(row, i, value)

    def set_column_cells(self, col, value):
        for i in range(self.size):
            self.set_cell(i, col, value)

    def update_nships(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.get_value(row, col) != None and self.get_value(row, col).upper() == "T":
                    for i in range(1, 4):
                        if self.get_value(row+i, col) != None and self.get_value(row+i, col).upper() == "B":
                            self.ships[i] -= 1
                            break
                        elif self.get_value(row+i, col) == None:
                            break
                elif self.get_value(row, col) != None and self.get_value(row, col).upper() == "L":
                    for i in range(1, 4):
                        if self.get_value(row, col+i) != None and self.get_value(row, col+i).upper() == "R":
                            self.ships[i] -= 1
                            break
                        elif self.get_value(row+i, col) == None:
                            break
                if self.get_value(row, col) != None and self.get_value(row, col).upper() == "C":
                    self.ships[0] -= 1


    def ship_fits(self, row, col, size, orientation):
        """ sets a ship on the board with origin in (row, col) and orientation H or V """
        for i in range(size):
            if orientation == "H":
                if col+i >= self.size or self.get_value(row, col+i) != None or self.row_values[row] < size or \
                (self.get_value(row-1, col) != None and self.get_value(row-1, col).upper() != "W") or \
                (self.get_value(row+1, col) != None and self.get_value(row+1, col).upper() != "W"):
                    return False
            elif orientation == "V":
                if row+i >= self.size or self.get_value(row+i, col) != None or self.col_values[col] < size or \
                (self.get_value(row, col-1) != None and self.get_value(row, col-1).upper() != "W") or \
                (self.get_value(row, col+1) != None and self.get_value(row, col+1).upper() != "W"):
                    return False
            elif orientation == "C":
                if self.row_values[row] == 0 or self.col_values[col] == 0 or \
                (row-1 >= 0 and self.get_value(row-1, col) != None and self.get_value(row-1, col).upper() != "W") or \
                (row+1 < self.size and self.get_value(row+1, col) != None and self.get_value(row+1, col).upper() != "W") or \
                (col-1 >= 0 and self.get_value(row, col-1) != None and self.get_value(row, col-1).upper() != "W") or \
                (col+1 < self.size and self.get_value(row, col+1) != None and self.get_value(row, col+1).upper() != "W"):
                    return False
        return True

    # can make it better by cheking the M cells and their directions
    def cell_fits(self, row, col, ship_type):

        if ship_type == "new_ship" and \
        ((self.get_value(row-2, col) != None and self.get_value(row-2, col).upper() == "T") or \
        (self.get_value(row+2, col) != None and self.get_value(row+2, col).upper() == "B") or \
        (self.get_value(row, col+2) != None and self.get_value(row, col+2).upper() == "R") or \
        (self.get_value(row, col-2) != None and self.get_value(row, col-2).upper() == "L") or \
        (self.get_value(row-1, col) != None and self.get_value(row-1, col).upper() != "W") or \
        (self.get_value(row+1, col) != None and self.get_value(row+1, col).upper() != "W") or \
        (self.get_value(row, col-1) != None and self.get_value(row, col-1).upper() != "W") or \
        (self.get_value(row, col+1) != None and self.get_value(row, col+1).upper() != "W") or \
        self.get_value(row, col) != None or row < 0 or col < 0 or row == self.size or col == self.size):
            return False

        elif ship_type == "top_ship" and \
        ((self.get_value(row+2, col) != None and self.get_value(row+2, col).upper() == "B") or \
        (self.get_value(row, col+2) != None and self.get_value(row, col+2).upper() == "R") or \
        (self.get_value(row, col-2) != None and self.get_value(row, col-2).upper() == "L") or \
        (self.get_value(row+1, col) != None and self.get_value(row+1, col).upper() != "W") or \
        (self.get_value(row, col-1) != None and self.get_value(row, col-1).upper() != "W") or \
        (self.get_value(row, col+1) != None and self.get_value(row, col+1).upper() != "W") or \
        self.get_value(row, col) != None or row < 0 or col < 0 or row == self.size or col == self.size):
            return False

        elif ship_type == "bottom_ship" and\
        ((self.get_value(row-2, col) != None and self.get_value(row-2, col).upper() == "T") or \
        (self.get_value(row, col+2) != None and self.get_value(row, col+2).upper() == "R") or \
        (self.get_value(row, col-2) != None and self.get_value(row, col-2).upper() == "L") or \
        (self.get_value(row-1, col) != None and self.get_value(row-1, col).upper() != "W") or \
        (self.get_value(row, col-1) != None and self.get_value(row, col-1).upper() != "W") or \
        (self.get_value(row, col+1) != None and self.get_value(row, col+1).upper() != "W") or \
        self.get_value(row, col) != None or row < 0 or col < 0 or row == self.size or col == self.size):
            return False

        elif ship_type == "left_ship" and \
        ((self.get_value(row-2, col) != None and self.get_value(row-2, col).upper() == "T") or \
        (self.get_value(row+2, col) != None and self.get_value(row+2, col).upper() == "B") or \
        (self.get_value(row, col+2) != None and self.get_value(row, col+2).upper() == "R") or \
        (self.get_value(row-1, col) != None and self.get_value(row-1, col).upper() != "W") or \
        (self.get_value(row+1, col) != None and self.get_value(row+1, col).upper() != "W") or \
        (self.get_value(row, col+1) != None and self.get_value(row, col+1).upper() != "W") or \
        self.get_value(row, col) != None or row < 0 or col < 0 or row == self.size or col == self.size):
            return False

        elif ship_type == "right_ship" and \
        ((self.get_value(row-2, col) != None and self.get_value(row-2, col).upper() == "T") or \
        (self.get_value(row+2, col) != None and self.get_value(row+2, col).upper() == "B") or \
        (self.get_value(row, col-2) != None and self.get_value(row, col-2).upper() == "L") or \
        (self.get_value(row-1, col) != None and self.get_value(row-1, col).upper() != "W") or \
        (self.get_value(row+1, col) != None and self.get_value(row+1, col).upper() != "W") or \
        (self.get_value(row, col-1) != None and self.get_value(row, col-1).upper() != "W") or \
        self.get_value(row, col) != None or row < 0 or col < 0 or row == self.size or col == self.size):
            return False

        return True

    def get_ships(self, row, col):
        ships = []


        if self.get_value(row, col) == None:
            #check unitary ship
            if self.col_values[col] == 0 or self.row_values[row] == 0:
                return None
            if self.cell_fits(row, col, "new_ship") and self.ships[0] > 0:
                ships.append((row, col, 1, "C"))
            else:
                return None

            # check horizontal ship
            if self.row_values[row] > 1:
                for i in range(1, min(self.row_values[row], 4)):
                    if self.cell_fits(row, col+i, "new_ship") and self.ships[i] > 0:
                        ships.append((row, col, i+1, "H"))
                    else:
                        break


            # check vertical ship
            if self.col_values[col] > 1:
                for i in range(1, min(self.col_values[col], 4)):
                    if self.cell_fits(row+i, col, "new_ship") and self.ships[i] > 0:
                        ships.append((row, col, i+1, "V"))
                    else:
                        break



        elif self.get_value(row, col).upper() == "T":
            for i in range(1, min(self.col_values[col]+1, 4)):
                if self.cell_fits(row+i, col, "top_ship") and self.ships[i] > 0:
                    ships.append((row, col, i+1, "V"))
                else:
                    break

            
        elif self.get_value(row, col).upper() == "B":
            for i in range(1, min(self.col_values[col]+1, 4)):
                if self.cell_fits(row-i, col, "bottom_ship") and self.ships[i] > 0:
                    ships.append((row-i+1, col, i+1, "V"))
                else:
                    break
        
        elif self.get_value(row, col).upper() == "L":
            for i in range(1, min(self.row_values[row]+1, 4)):
                if self.cell_fits(row, col+i, "left_ship") and self.ships[i] > 0:
                    ships.append((row, col, i+1, "H"))
                else:
                    break
 
        elif self.get_value(row, col).upper() == "M":
            # ships fit horizontaly with the "M"
            if (self.get_value(row-1, col) != None and self.get_value(row-1, col).upper() == "W") or\
            (self.get_value(row+1, col) != None and self.get_value(row+1, col).upper() == "W"):
                ships.append((row, col-1, 3, "H"))
                if self.row_values[row] >= 3:
                    if self.cell_fits(row, col-2, "new_ship"):
                        ships.append((row, col-2, 4, "H"))
                    if self.cell_fits(row, col+2, "new_ship"):
                        ships.append((row, col-1, 4, "H"))


            # ships fit verticaly with the "M"
            elif (self.get_value(row, col-1) != None and self.get_value(row, col-1).upper() == "W") or\
            (self.get_value(row, col+1) != None and self.get_value(row, col+1).upper() == "W"):
                ships.append((row-1, col, 3, "V"))
                if self.row_values[row] >= 3:
                    if self.cell_fits(row-2, col, "new_ship"):
                        ships.append((row-2, col, 4, "V"))
                    if self.cell_fits(row+2, col, "new_ship"):
                        ships.append((row-1, col, 4, "V"))

            # find both vertical and horizontal ships with the "M"
            else:
                ships.append((row, col-1, 3, "H"))
                ships.append((row-1, col, 3, "V"))

                if self.row_values[row] >= 3:
                    if self.cell_fits(row, col-2, "new_ship"):
                        ships.append((row, col-2, 4, "H"))
                    if self.cell_fits(row, col+2, "new_ship"):
                        ships.append((row, col-1, 4, "H"))

                if self.row_values[row] >= 3:
                    if self.cell_fits(row-2, col, "new_ship"):
                        ships.append((row-2, col, 4, "V"))
                    if self.cell_fits(row+2, col, "new_ship"):
                        ships.append((row-1, col, 4, "V"))


        return ships


    def set_values(self, row_values, col_values):
        self.row_values = row_values
        self.col_values = col_values

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return None
        value = self.grid[row][col]
        return value

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row+1 >= self.size or row-1 < 0:
            return (None, None)
        first,second = self.grid[row - 1][col], self.grid[row + 1][col]
        return (first,second)

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col+1 >= self.size or col-1 < 0:
            return (None, None)
        first,second = self.grid[row][col - 1], self.grid[row][col + 1]
        return (first,second)

    def print_board(self):
        for row in self.grid:
            for cell in row:
                if cell is None:
                    print(".", end=" ")
                else:
                    print(cell, end=" ")
            print()


    def water_on_zero_values(self):
        # check number of cells in each collumn and each row and compare to the restriction
        for i in range(self.size):
            if self.row_values[i] == 0:
                self.set_row_cells(i, "w")
            if self.col_values[i] == 0:
                self.set_column_cells(i, "w")

    def check_mandatory_ship(self, row, col, value):
        if value == "T":

            if row+1 == self.size-1:
                self.set_cell(row+1, col, "b")
                self.set_cell(row+1, col-1, "w")
                self.set_cell(row+1, col+1, "w")
            elif self.get_value(row+1, col) != None and self.get_value(row+1, col).upper() == "M" and \
                self.col_values[col] == 1:
                self.set_cell(row+2, col, "b")
                self.set_cell(row+3, col, "w")
                self.set_cell(row+3, col-1, "w")
                self.set_cell(row+3, col+1, "w")
            elif self.col_values[col] == 1 and self.get_value(row+1, col) == None:
                self.set_cell(row+1, col, "b")
                self.set_cell(row+2, col, "w")
                self.set_cell(row+2, col-1, "w")
                self.set_cell(row+2, col+1, "w")
            else:
                for i in range(1, 4):
                    if self.get_value(row+i, col) != None and self.get_value(row+i, col).upper() == "B":
                        for j in range(0, i):
                            self.set_cell(row+j, col, "m")
                            self.set_cell(row+j, col-1, "w")
                            self.set_cell(row+j, col+1, "w")
                    if self.get_value(row+i, col) != None and self.get_value(row+i, col).upper() == "W":
                        for w in range(1, i-1):
                            self.set_cell(row+w, col, "m")
                            self.set_cell(row+w, col-1, "w")
                            self.set_cell(row+w, col+1, "w")
                        self.set_cell(row+i-1, col, "b")
                if self.get_value(row+2, col) != None and self.get_value(row+2, col).upper() == "M":
                    self.set_cell(row+1, col, "m")
                    self.set_cell(row+1, col-1, "w")
                    self.set_cell(row+1, col+1, "w")
                    self.set_cell(row+3, col, "b")
                    self.set_cell(row+3, col-1, "w")
                    self.set_cell(row+3, col+1, "w")
                    self.set_cell(row+4, col-1, "w")
                    self.set_cell(row+4, col, "w")
                    self.set_cell(row+4, col+1, "w")


        elif value == "B":
            if row-1 == 0:
                self.set_cell(row-1, col, "t")
                self.set_cell(row-1, col-1, "w")
                self.set_cell(row-1, col+1, "w")

            elif self.get_value(row-1, col) != None and self.get_value(row-1, col).upper() == "M" and \
                self.col_values[col] == 1:
                self.set_cell(row-2, col, "b")
                self.set_cell(row-3, col, "w")
                self.set_cell(row-3, col-1, "w")
                self.set_cell(row-3, col+1, "w")

            elif self.col_values[col] == 1 and self.get_value(row-1, col) == None:
                self.set_cell(row-1, col, "t")
                self.set_cell(row-2, col, "w")
                self.set_cell(row-2, col-1, "w")
                self.set_cell(row-2, col+1, "w")

            elif self.get_value(row-2, col) != None and self.get_value(row-2, col).upper() == "M":
                    self.set_cell(row-1, col, "m")
                    self.set_cell(row-1, col-1, "w")
                    self.set_cell(row-1, col+1, "w")
                    self.set_cell(row-3, col, "t")
                    self.set_cell(row-3, col-1, "w")
                    self.set_cell(row-3, col+1, "w")
                    self.set_cell(row-4, col-1, "w")
                    self.set_cell(row-4, col, "w")
                    self.set_cell(row-4, col+1, "w")

        elif value == "L":
            if col+1 == self.size-1:
                self.set_cell(row, col+1, "r")
                self.set_cell(row-1, col+1, "w")
                self.set_cell(row+1, col+1, "w")

            elif self.get_value(row, col+1) != None and self.get_value(row, col+1) == "M" and \
                self.row_values[row] == 1:
                self.set_cell(row, col+2, "r")
                self.set_cell(row-1, col+2, "w")
                self.set_cell(row+1, col+2, "w")
                self.set_cell(row-1, col+3, "w")
                self.set_cell(row-1, col+3, "w")
                self.set_cell(row-1, col+3, "w")
            elif self.row_values[row] == 1 and self.get_value(row, col+1) == None:
                self.set_cell(row, col+1, "r")
                self.set_cell(row-1, col+2, "w")
                self.set_cell(row, col+2, "w")
                self.set_cell(row+1, col+2, "w")

            else:
                for i in range(1, 4):
                    if self.get_value(row, col+i) != None and self.get_value(row, col+i).upper() == "R":
                        for j in range(0, i):
                            set_cell(row, col+j, "m")
                            set_cell(row-1, col+j, "w")
                            set_cell(row+1, col+j, "w")
                if self.get_value(row, col+2) != None and self.get_value(row, col+2).upper() == "M":
                    self.set_cell(row, col+1, "m")
                    self.set_cell(row-1, col+1, "w")
                    self.set_cell(row+1, col+1, "w")
                    self.set_cell(row, col+2, "r")
                    self.set_cell(row-1, col+2, "w")
                    self.set_cell(row+1, col+2, "w")
                    self.set_cell(row-1, col+3, "w")
                    self.set_cell(row, col+3, "w")
                    self.set_cell(row+1, col+3, "w")

        elif value == "R":
            if col-1 == 0:
                self.set_cell(row, col-1, "l")
                self.set_cell(row-1, col-1, "w")
                self.set_cell(row+1, col-1, "w") 
            elif self.get_value(row, col-2) != None and self.get_value(row, col-2).upper() == "M":
                    self.set_cell(row, col-1, "m")
                    self.set_cell(row-1, col-1, "w")
                    self.set_cell(row+1, col-1, "w")
                    self.set_cell(row, col-2, "l")
                    self.set_cell(row-1, col-2, "w")
                    self.set_cell(row+1, col-2, "w")
                    self.set_cell(row-1, col-3, "w")
                    self.set_cell(row, col-3, "w")
                    self.set_cell(row+1, col-3, "w")
            elif self.row_values[row] == 1 and self.get_value(row, col-1) == None:
                self.set_cell(row, col-1, "l")
                self.set_cell(row-1, col-2, "w")
                self.set_cell(row, col-2, "w")
                self.set_cell(row+1, col-2, "w")
            elif self.get_value(row, col-1) != None and self.get_value(row, col-1) == "M" and \
                self.row_values[row] == 1:
                self.set_cell(row, col-2, "l")
                self.set_cell(row-1, col-2, "w")
                self.set_cell(row+1, col-2, "w")
                self.set_cell(row-1, col-3, "w")
                self.set_cell(row-1, col-3, "w")
                self.set_cell(row-1, col-3, "w")



    def mandatory_actions(self):
        """Devolve uma lista de todas as ações obrigatórias a
        partir de um determinado estado passado como argumento."""

        for row in range(self.size):
            for col in range(self.size):
                cell = self.get_value(row, col)
                if cell != None and cell.upper() != "W":
                    for i in range(row-1, row+2):
                        for j in range(col-1, col+2):
                            if i != row or j != col:
                                if cell.upper() == "T" and (i != row+1 or j != col):
                                    self.set_cell(i, j, "w")
                                elif cell.upper() == "B" and (i != row-1 or j != col):
                                    self.set_cell(i, j, "w")
                                elif cell.upper() == "R" and (i != row or j != col-1):
                                    self.set_cell(i, j, "w")
                                elif cell.upper() == "L" and (i != row or j != col+1):
                                    self.set_cell(i, j, "w")
                                elif cell.upper() == "C":
                                    self.set_cell(i, j, "w")
                                elif cell.upper() == "M" and i != row and j != col:
                                    self.set_cell(i, j, "w")
                    self.check_mandatory_ship(row, col, cell.upper())
                
                    if cell.upper() == "M":
                        top, down = self.adjacent_vertical_values(row, col)
                        left, right = self.adjacent_horizontal_values(row, col)

                        if (top != None and top.upper() == "W") or (down != None and down.upper() == "W") or \
                        col-1 == 0 or col+1 == self.size:
                            self.set_cell(row-1, col, "w")
                            self.set_cell(row+1, col, "w")

                            if col-1 == 0:
                                self.set_cell(row, col-1, "l")
                            elif col+1 == self.size:
                                self.set_cell(row, col+1, "r")

                        elif (left != None and left.upper == "W") or (right != None and right.upper() == "W") or \
                        row-1 == 0 or row + 1 == self.size:
                            self.set_cell(row, col-1, "w")
                            self.set_cell(row, col+1, "w")

                            if row-1 == 0:
                                self.set_cell(row-1, col, "t")
                            elif row+1 == self.size:
                                self.set_cell(row+1, col, "b")



    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        """

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
            row = int(row)
            col = int(col)
            board.set_cell(row, col, hint_value)


        board.water_on_zero_values()
        board.mandatory_actions()
        board.water_on_zero_values()
        board.mandatory_actions()
        board.water_on_zero_values()
        board.update_nships()

        return board


    # TODO: outros metodos da classe



class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""

        # criar array the states?
        super().__init__(BimaruState(board))
        #self.board = board

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        actions = []

        for row in range(state.board.size):
            for col in range(state.board.size):
                if state.board.get_value(row, col) == None or \
                (state.board.get_value(row, col) != None and state.board.get_value(row, col).upper() != "W"):
                    ships_in_position = state.board.get_ships(row, col)
                    if ships_in_position != None:
                        for ship in ships_in_position:
                            actions.append(ship)
        return actions

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""


        #print(action)

        new_board = Board(state.board.size)
        new_board.grid = copy.deepcopy(state.board.grid)
        new_board.size = copy.deepcopy(state.board.size)
        new_board.row_values = copy.deepcopy(state.board.row_values)
        new_board.col_values = copy.deepcopy(state.board.col_values)
        new_board.ships = copy.deepcopy(state.board.ships)
        new_state = BimaruState(new_board)

        row = action[0]
        col = action[1]
        size = action[2]
        orientation = action[3]

        if orientation == "C":
            new_state.board.set_cell(row, col, "c")
            new_state.board.set_cell(row, col-1, "w")
            new_state.board.set_cell(row, col+1, "w")
            new_state.board.set_cell(row-1, col-1, "w")
            new_state.board.set_cell(row-1, col, "w")
            new_state.board.set_cell(row-1, col+1, "w")
            new_state.board.set_cell(row+1, col-1, "w")
            new_state.board.set_cell(row+1, col, "w")
            new_state.board.set_cell(row+1, col+1, "w")

        elif orientation == "H":
            new_state.board.set_cell(row, col, "l")
            new_state.board.set_cell(row-1, col, "w")
            new_state.board.set_cell(row+1, col, "w")
            new_state.board.set_cell(row-1, col-1, "w")
            new_state.board.set_cell(row, col-1, "w")
            new_state.board.set_cell(row+1, col-1, "w")

            for i in range(1, size-1):
                new_state.board.set_cell(row, col+i, "m")
                new_state.board.set_cell(row-1, col+i, "w")
                new_state.board.set_cell(row+1, col+i, "w")
            new_state.board.set_cell(row, col+size-1, "r")
            new_state.board.set_cell(row-1, col+size-1, "w")
            new_state.board.set_cell(row+1, col+size-1, "w")
            new_state.board.set_cell(row-1, col+size, "w")
            new_state.board.set_cell(row, col+size, "w")
            new_state.board.set_cell(row+1, col+size, "w")

        elif orientation == "V":
            new_state.board.set_cell(row, col, "t")
            new_state.board.set_cell(row, col-1, "w")
            new_state.board.set_cell(row, col+1, "w")
            new_state.board.set_cell(row-1, col-1, "w")
            new_state.board.set_cell(row-1, col+1, "w")
            new_state.board.set_cell(row-1, col, "w")

            for i in range(1, size-1):
                new_state.board.set_cell(row+i, col, "m")
                new_state.board.set_cell(row+i, col-1, "w")
                new_state.board.set_cell(row+i, col+1, "w")
            new_state.board.set_cell(row+size-1, col, "b")
            new_state.board.set_cell(row+size-1, col-1, "w")
            new_state.board.set_cell(row+size-1, col+1, "w")
            new_state.board.set_cell(row+size, col-1, "w")
            new_state.board.set_cell(row+size, col, "w")
            new_state.board.set_cell(row+size, col+1, "w")

        new_state.board.ships[size-1] -= 1

        return new_state


    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        for i in range(state.board.size):
            if state.board.row_values[i] > 0:
                return False
            if range(state.board.col_values[i] > 0):
                return False
        for ship in state.board.ships:
            if ship != 0:
                return False
        return True


    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe



if __name__ == "__main__":
    board = Board.parse_instance()
    board.mandatory_actions()
    board.print_board()
    bimaru = Bimaru(board)
    solution = depth_first_tree_search(bimaru)
    solution.state.board.print_board()
    #bimaru.board.mandatory_actions()
    #bimaru.board.print_board()
    #actions = bimaru.actions(BimaruState(bimaru.board))
    #new_state = bimaru.result(BimaruState(bimaru.board), actions[4])
    #new_state.board.print_board()
    #for action in actions:
    #    print(action)

    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
