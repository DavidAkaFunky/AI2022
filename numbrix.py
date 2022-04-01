# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 03:
# 95550 David Belchior
# 95562 Diogo Santos

import sys
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search
from copy import deepcopy

class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id


class Board:
    """ Representação interna de um tabuleiro de Numbrix. """

    def __init__(self, board: list, dim: int) -> None:
        self.board = board
        self.dim = dim

    def get_board(self) -> list:
        return self.board

    def get_dim(self) -> int:
        return self.dim

    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """

        return self.board[row][col]

    def get_numbers(self):
        """ Devolve uma lista com todos os valores do tabuleiro. """

        return [number for row in self.board for number in row]

    def get_missing_numbers(self):
        """ Devolve uma lista com todos os valores que faltam no tabuleiro. """

        return [number for number in range(1, self.dim**2+1) if number not in self.get_numbers()]

    def get_number_seq(self, number: int) -> tuple:
        """ Devolve uma lista com todos os valores imediatamente adjacentes ao numero. """

        res = []

        if number > 1:
            res.append(number-1)
        if number < self.dim**2:
            res.append(number+1)

        return res

    def is_valid_number(self, row: int, col: int, number: int):
        """ Verifica se o numero é valido para a respetiva posicao."""

        valid_neighbours = []
        # Para valor vizinho
        for neighbour in self.get_neighbours(row, col):
            # Adiciona valores adjacentes
            valid_neighbours += self.get_number_seq(neighbour)

        # é um valor valido se pertencer à lista de valores adjacentes dos vizinhos
        return number in valid_neighbours

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """

        numbers = ()
        for x in (row-1, row+1):
            if x < 0 or x >= self.dim:
                numbers += (None,)
            else:
                numbers += (self.get_number(x, col),)
        return numbers

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """

        numbers = ()
        for y in (col-1, col+1):
            if y < 0 or y >= self.dim:
                numbers += (None,)
            else:
                numbers += (self.get_number(row, y),)
        return numbers

    def get_neighbours(self, row: int, col: int) -> tuple:
        """ Devolve os valores vizinhos da respetiva posição. """

        neighbours = self.adjacent_vertical_numbers(row, col) + self.adjacent_horizontal_numbers(row, col)
        return tuple(filter(lambda n: n != None, neighbours))

    def get_available_positions(self, row: int, col: int):
        """ Devolve as posicoes que estao por preencher em redor
        da respetiva posicao. """

        available_positions = ()
        for y in (col-1, col+1):
            if y >= 0 and y < self.dim and self.get_number(row, y) == 0:
                available_positions += ((row, y),)
        for x in (row-1, row+1):
            if x >= 0 and x < self.dim and self.get_number(x, col) == 0:
                available_positions += ((x, col),)

        return available_positions

    def get_actions(self, row: int, col: int):
        """ Devolve uma lista de acoes possiveis de realizar na resptiva posicao. """

        actions = []
        for number in self.get_missing_numbers():
            if self.is_valid_number(row, col, number):
                actions.append((row, col, number))

        return actions

    def add_number(self, row: int, col: int, number: int) -> None:
        """ Atualiza o valor na respetiva posicao do tabuleiro ."""
        new_board = deepcopy(self)
        new_board.board[row][col] = number
        return new_board

    def print_board(self):
        """ Imprime o tabuleiro na consola. """

        for row in self.board:
            print("\t".join([str(number) for number in row]))

    @staticmethod
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """

        with open(filename, "r") as f:
            lines = f.readlines()
            dim = int(lines[0])
            lines = lines[1:]
            assert(len(lines) == dim)
            board = []
            for line in lines:
                line = line.strip().split("\t")
                assert(len(line) == dim)
                board.append([int(x) for x in line])
        return Board(board, dim)


class Numbrix(Problem):

    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """

        self.initial = NumbrixState(board)


    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """

        board = state.board
        dim = board.get_dim()

        # Acoes disponiveis
        total_actions = ()
        # Para cada posicao
        for row in range(dim):
            for col in range(dim):
                # Se a posicao está vazia
                if board.get_number(row, col) == 0:
                    # Obtem todas as acoes dessa posicao
                    actions = board.get_actions(row, col)
                    for action in actions:
                        total_actions += (action,)
                        
        return total_actions


    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        new_state = deepcopy(state)
        new_state.board = new_state.board.add_number(action[0], action[1], action[2])
        return new_state

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        
        boardd = state.board
        dim = boardd.get_dim()

        # Para cada posicao
        for row in range(dim):
            for col in range(dim):
                # Obtem os vizinhos e os valores adjacentes
                neighbours = boardd.get_neighbours(row, col)
                number_seq = boardd.get_number_seq(boardd.get_number(row, col))
                # Se um dos valores adjacentes nao for um vizinho da posicao
                # entao nao forma uma sequencia e falha
                for number in number_seq:
                    if number not in neighbours:
                        return False

        return True


    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        return 0

def main():
    # Lê tabuleiro do ficheiro
    board = Board.parse_instance(sys.argv[1])

    # Cria uma instancia de Numbrix
    problem = Numbrix(board)

    # Obtem o nó solução usando A*
    goal_node = astar_search(problem, display=True)

    problem.initial.board.print_board()
    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:")
    goal_node.state.board.print_board()

if __name__ == "__main__":
    main()