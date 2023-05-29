# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 46:
# 102543 Pedro Noronha
# 00000 Mariana Carvalho

import sys
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
        self.boats = {4, 3, 3, 2, 2, 2, 1, 1, 1, 1}

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

    def set_ship(self, row, col, size, orientation):
        """ sets a ship on the board with origin in (row, col) and orientation H or V """
        for i in range(size):
            if orientation == "H":
                set_cell(row, col+i, "S")
            elif orientation == "V":
                set_cell(row+1, col, "S")

    def ship_fits(self, row, col, size, orientation):
        """ sets a ship on the board with origin in (row, col) and orientation H or V """
        for i in range(size):
            if orientation == "H":
                if col+i >= self.size or self.get_value(row, col+i) != None or self.row_values[row] < size:
                    return False
            elif orientation == "V":
                if row+i >= self.size or self.get_value(row+i, col) != None or self.col_values[col] < size:
                    return False
            elif orientation == "C":
                if self.row_values[row] == 0 or self.col_values[col] == 0 or \
                (row-1 >= 0 and self.get_value(row-1, col) != None and self.get_value(row-1, col).upper() != "W") or \
                (row+1 < self.size and self.get_value(row+1, col) != None and self.get_value(row+1, col).upper() != "W") or \
                (col-1 >= 0 and self.get_value(row, col-1) != None and self.get_value(row, col-1).upper() != "W") or \
                (col+1 < self.size and self.get_value(row, col+1) != None and self.get_value(row, col+1).upper() != "W"):
                    return False
        return True

    def set_values(self, row_values, col_values):
        self.row_values = row_values
        self.col_values = col_values

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
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


    def update_row_col_values(self):
        # check number of cells in each collumn and each row and compare to the restriction
        for i in range(self.size):
            if self.row_values[i] == 0:
                self.set_row_cells(i, "w")
            if self.col_values[i] == 0:
                self.set_column_cells(i, "w")
            """
            row_ship_count = sum(1 for j in range(self.size) if self.get_value(i, j) not in [None, "W", "w"])
            col_ship_count = sum(1 for j in range(self.size) if self.get_value(j, i) not in [None, "W", "w"])
            if row_ship_count >= self.row_values[i]:
                self.set_row_cells(i, 'w')
            self.row_values[i] -= row_ship_count
            if col_ship_count >= self.col_values[i]:
                self.set_column_cells(i, 'w')
            self.col_values[i] -= col_ship_count
            """


    def mandatory_actions(self):
        """Devolve uma lista de todas as ações obrigatórias a
        partir de um determinado estado passado como argumento."""

        for row in range(self.size):
            for col in range(self.size):
                cell = self.get_value(row, col)
                if cell != None and cell != "W":
                    for i in range(row-1, row+2):
                        for j in range(col-1, col+2):
                            if i != row or j != col:
                                if cell == "T" and (i != row+1 or j != col):
                                    self.set_cell(i, j, "w")
                                elif cell == "B" and (i != row-1 or j != col):
                                    self.set_cell(i, j, "w")
                                elif cell == "R" and (i != row or j != col-1):
                                    self.set_cell(i, j, "w")
                                elif cell == "L" and (i != row or j != col+1):
                                    self.set_cell(i, j, "w")
                                elif cell == "C":
                                    self.set_cell(i, j, "w")
                                elif cell == "M" and i != row and j != col:
                                    self.set_cell(i, j, "w")
                
                    if cell == "M":
                        top, down = self.adjacent_vertical_values(row, col)
                        left, right = self.adjacent_horizontal_values(row, col)

                        if (top != None and top.upper() == "W") or (down != None and down.upper() == "W") or \
                        col-1 == 0 or col+1 == self.size:
                            self.set_cell(row, col-1, "w")
                            self.set_cell(row, col+1, "w")
                        elif (down != None and down.upper == "W") or (right != None and right.upper() == "W") or \
                        row-1 == 0 or row + 1 == self.size:
                            self.set_cell(row-1, col, "w")
                            self.set_cell(row+1, col, "w")


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

        board.update_row_col_values()

        return board


    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""

        # criar array the states?
        super().__init__(board)    
        #self.board = board

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        actions = []

        for row in range(state.board.size):
            for col in range(state.board.size):
                if state.board.get_value(row, col) == None:
                    if state.board.ship_fits(row, col, 1, "C"):
                        actions.append((row, col, 1, "C"))
                    else:
                        break
                    for size in range(2, 5):
                        if state.board.ship_fits(row, col, size, "H"):
                            actions.append((row, col, size, "H"))
                        if state.board.ship_fits(row, col, size, "V"):
                            actions.append((row, col, size, "V"))

        return actions

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        new_state = BimaruState(state.board)

        row = action[0]
        col = action[1]

        if action[3] == "V":
            for row in range(action[2]-1):
                top, down = new_state.board.adjacent_vertical_values(row, col)
                if top == None or top.upper() == "W":
                    new_state.board.set_cell(row, col, "t")
                else:
                    new_state.board.set_cell(row, col, "m")

            if new_state.board.get_value(action[0]+action[2], col) != None and \
            (new_state.board.get_value(action[0]+action[2], col).upper() == "B" or \
                new_state.board.get_value(action[0]+action[2], col).upper() == "M"):
                new_state.board.set_cell(action[0]+action[2]-1, col, "m")
            else:
                new_state.board.set_cell(action[0]+action[2]-1, col, "b")


        elif action[3] == "H":
            for col in range(action[2]-1):
                left, right = new_state.board.adjacent_horizontal_values(row, col)
                if left == None or left.upper() == "W":
                    new_state.board.set_cell(row, col, "l")
                else:
                    new_state.board.set_cell(row, col, "m")
            
            if new_state.board.get_value(row, action[1]+action[2]) != None and \
            (new_state.board.get_value(row, action[1]+action[2]).upper() == "R" or \
                new_state.board.get_value(row, action[1]+action[2]).upper() == "M"):
                new_state.board.set_cell(row, action[1]+action[2]-1, "m")
            else:
                new_state.board.set_cell(row, action[1]+action[2]-1, col, "r")

        elif action[3] == "C":
            new_state.board.set_cell(action[0], action[1], "c")

        return new_state


    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        for i in range(state.size):
            if state.row_values[i] != 0:
                return False
            if state.col_values[i] != 0:
                return False
        return True


    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()
    #board.print_board()
    bimaru = Bimaru(board)
    solution = depth_first_tree_search(bimaru)
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
