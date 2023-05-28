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

    def set_cell(self, row, col, value):
        # check if it legal to set this cell
        if row >= 0 and row < self.size and col >= 0 and col < self.size and self.get_value(row, col) == None:
            self.grid[row][col] = value

    def set_ship(self, row, col, size, orientation):
        """ sets a ship on the board with origin in (row, col) and orientation H or V """
        for i in range(size):
            if orientation == "H":
                set_cell(row, col+i, "S")
            elif orientation == "V":
                set_cell(row+1, col, "S")

    def ship_fits(self, row, col, orientation):
        """ sets a ship on the board with origin in (row, col) and orientation H or V """
        for i in range(size):
            if orientation == "H":
                if col+i >= self.size or get_value(row, col+i) != None:
                    return False
            elif orientation == "V":
                if row+i >= self.size or get_value(row+i, col) != None:
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
        first,second = self.grid[row - 1][col], self.grid[row + 1][col]
        return (first,second)

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
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

        return board


    # TODO: outros metodos da classe


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""

        self.board = board

    def mandatory_actions(self, state: BimaruState):
        """Devolve uma lista de todas as ações obrigatórias a
        partir de um determinado estado passado como argumento."""

        mandatory_actions = []

        for row in range(state.board.size):
            for col in range(state.board.size):
                cell = state.board.get_value(row, col)
                if cell != None and cell != "W":
                    for i in range(row-1, row+2):
                        for j in range(col-1, col+2):
                            if i != row or j != col:
                                if cell == "T" and (i != row+1 or j != col):
                                    self.board.set_cell(i, j, "w")
                                    mandatory_actions.append((i, j, "w"))
                                elif cell == "B" and (i != row-1 or j != col):
                                    self.board.set_cell(i, j, "w")
                                    mandatory_actions.append((i, j, "w"))
                                elif cell == "R" and (i != row or j != col-1):
                                    self.board.set_cell(i, j, "w")
                                    mandatory_actions.append((i, j, "w"))
                                elif cell == "L" and (i != row or j != col+1):
                                    self.board.set_cell(i, j, "w")
                                    mandatory_actions.append((i, j, "w"))
                                elif cell == "C":
                                    self.board.set_cell(i, j, "w")
                                    mandatory_actions.append((i, j, "w"))
                                elif cell == "M" and i != row and j != col:
                                    self.board.set_cell(i, j, "w")
                
                    if cell == "M":
                        top, down = state.board.adjacent_vertical_values(row, col)
                        left, right = state.board.adjacent_horizontal_values(row, col)
                        if (top != None and top != "W") or (down != None and down != "W"):
                            self.board.set_cell(row, col-1, "w")
                        elif (left != None and left != "W") or (right != None and right != "W"):
                            self.board.set_cell(row-1, col, "w")
                            self.board.set_cell(row+1, col, "w")


        for i in range(state.board.size):
            if state.board.row_values[i] == 0:
                for j in range(state.board.size):
                    self.board.set_cell(i, j, "w")
            if state.board.col_values[i] == 0:
                for j in range(state.board.size):
                    self.board.set_cell(j, i, "w")


        def actions(self, state: BimaruState):
            """Retorna uma lista de ações que podem ser executadas a
            partir do estado passado como argumento."""

            actions = []

            for row in range(state.board.size):
                for col in range(state.board.size):
                    if state.board.get_value(row, col) == None:
                        for size in range(1, 4):
                            if state.board.size.ship_fits(row, col, size, "H"):
                                actions.append((row, col, size, "H"))
                            if state.board.size.ship_fits(row, col, size, "V"):
                                actions.append((row, col, size, "V"))


            return actions


    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    board = Board.parse_instance()
    board.print_board()
    bimaru = Bimaru(board)
    bimaru.mandatory_actions(BimaruState(board))
    bimaru.board.print_board()

    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
