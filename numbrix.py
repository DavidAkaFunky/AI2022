# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 03:
# 95550 David Belchior
# 95562 Diogo Santos

import sys
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_graph_search, \
    depth_first_tree_search, greedy_search, recursive_best_first_search
from copy import deepcopy
from utils import manhattan_distance
from time import sleep

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
        self.empty_pos = []
        self.missing_numbers = {x: [False, False] for x in range(1, self.dim ** 2 + 1)}
        self.positions = {}
        self.missing_numbers[1][0] = True
        self.missing_numbers[dim**2][1] = True
        for row in range(dim):
            for col in range(dim):
                number = board[row][col]
                if number == 0:
                    self.empty_pos.append((row, col))
                else:
                    try:
                        self.missing_numbers[number-1][1] = True
                    except KeyError:
                        pass
                    try:
                        self.missing_numbers[number+1][0] = True
                    except KeyError:
                        pass
                    self.positions[number] = (row, col)
                    self.missing_numbers.pop(number)
        self.number_empty = len(self.missing_numbers)

    def get_empty_positions(self) -> list:
        return self.empty_pos

    def get_number_of_empty_spaces(self) -> int:
        return self.number_empty

    def get_board(self) -> list:
        return self.board

    def get_dim(self) -> int:
        return self.dim

    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """

        return self.board[row][col]

    def get_missing_numbers(self):
        """ Devolve uma lista com todos os valores que faltam no tabuleiro. """

        return self.missing_numbers

    def get_best_missing_number(self):
        chosen_alternative = False
        for number in self.missing_numbers:
            left = self.missing_numbers[number][0]
            right = self.missing_numbers[number][1]
            if left and right:
                return number
            if not chosen_alternative and (left or right) and number != 1 and number != self.dim**2:
                chosen_alternative = True
                alternative = number
        return alternative

    #def get_best_missing_number(self):
    #    number = self.missing_numbers[0]
    #    if len(self.missing_numbers) == 1 or self.missing_numbers[1] != number+1:
    #        return number
    #    chosen_alternative = False
    #    alternative = number
    #    for i in range(1, len(self.missing_numbers)-1):
    #        number = self.missing_numbers[i]
    #        left = number-1 != self.missing_numbers[i-1]
    #        right = number+1 != self.missing_numbers[i+1]
    #        if left and right:
    #            return number
    #        if not chosen_alternative and (left or right):
    #            chosen_alternative = True
    #            alternative = number
    #    return alternative
                

    def get_number_seq(self, number: int) -> tuple:
        """ Devolve uma lista com todos os valores imediatamente adjacentes ao numero. """

        res = []

        if number > 1:
            res.append(number - 1)
        if number < self.dim ** 2:
            res.append(number + 1)

        return res

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """

        numbers = ()
        for x in (row - 1, row + 1):
            if x < 0 or x >= self.dim:
                numbers += (None,)
            else:
                numbers += (self.get_number(x, col),)
        return numbers

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """

        numbers = ()
        for y in (col - 1, col + 1):
            if y < 0 or y >= self.dim:
                numbers += (None,)
            else:
                numbers += (self.get_number(row, y),)
        return numbers

    def get_neighbours(self, row: int, col: int):
        """ Devolve os valores vizinhos da respetiva posição. """

        neighbours = self.adjacent_vertical_numbers(row, col) + self.adjacent_horizontal_numbers(row, col)
        return filter(lambda n: n is not None, neighbours)

    def get_available_positions(self, row: int, col: int):
        """ Devolve as posicoes que estao por preencher em redor
        da respetiva posicao. """

        available_positions = set()
        for y in (col - 1, col + 1):
            if 0 <= y < self.dim and self.get_number(row, y) == 0:
                available_positions.add((row, y))
        for x in (row - 1, row + 1):
            if 0 <= x < self.dim and self.get_number(x, col) == 0:
                available_positions.add((x, col))

        return available_positions

    def add_number(self, row: int, col: int, number: int) -> None:
        """ Atualiza o valor na respetiva posicao do tabuleiro ."""
        self.number_empty -= 1
        self.board[row][col] = number
        self.missing_numbers.pop(number)
        self.empty_pos.remove((row, col))
        self.positions[number] = (row, col)
        try:
            self.missing_numbers[number-1][1] = True
        except KeyError:
            pass
        try:
            self.missing_numbers[number+1][0] = True
        except KeyError:
            pass

    def get_best_positions(self, number, max_seq) -> list:
        if max_seq == []:
            neighbours = self.empty_pos
        else:
            pos = self.positions[max_seq[0]]
            neighbours = self.get_available_positions(pos[0], pos[1])
            for _number in max_seq[1:]:
                pos = self.positions[_number]
                neighbours = neighbours & self.get_available_positions(pos[0], pos[1])
        #return neighbours
        positions = []
        for neighbour in neighbours:
            flag = True
            for position in self.positions:
                if abs(number-position) < manhattan_distance(self.positions[position], neighbour):
                    flag = False
                    break
            if flag:
                positions.append(neighbour)
        return positions

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
            assert len(lines) == dim
            board = []
            for line in lines:
                line = line.strip().split("\t")
                assert len(line) == dim
                board.append([int(x) for x in line])
        return Board(board, dim)


class Numbrix(Problem):

    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = NumbrixState(board)
        self.n = 0

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        board = state.board
        number = board.get_best_missing_number() # Não é eficiente
        #print(board.missing_numbers, number)
        #number = list(board.get_missing_numbers().keys())[0]
        max_seq = [x for x in board.get_number_seq(number) if x not in board.get_missing_numbers()]
        actions = [(row, col, number) for (row, col) in board.get_best_positions(number, max_seq)]
        if actions == []:
            self.n += 1
        #board.print_board()
        #print(actions)
        #print("______________________________")
        return actions

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        new_state = deepcopy(state)
        new_state.board.add_number(action[0], action[1], action[2])
        return new_state

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """

        return state.board.get_number_of_empty_spaces() == 0

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # return 0

        #return node.state.board.get_number_of_empty_spaces()
        
        total = 0
        board = node.state.board
        for space in board.get_empty_positions():
            total += (4-len(board.get_available_positions(space[0], space[1])))**2
        return total


def main():
    # Lê tabuleiro do ficheiro
    board = Board.parse_instance(sys.argv[1])

    # Cria uma instancia de Numbrix
    problem = Numbrix(board)

    # Obtem o nó solução usando A*
    #goal_node = depth_first_tree_search(problem)
    #goal_node = greedy_search(problem, problem.h)
    goal_node = astar_search(problem, display=True)  # 8 Memory Limit
    #goal_node = recursive_best_first_search(problem)  # 7 Time Limit
    print(problem.n)
    # Mostra tabuleiro final
    goal_node.state.board.print_board()


if __name__ == "__main__":
    main()
