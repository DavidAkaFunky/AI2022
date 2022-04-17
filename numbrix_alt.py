# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 03:
# 95550 David Belchior
# 95562 Diogo Santos

import sys

from numpy import diff
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_graph_search, \
    depth_first_tree_search, greedy_search, recursive_best_first_search
from copy import deepcopy
from utils import manhattan_distance

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

        # Basic board attributes
        
        self.board = board                        
        self.dim = dim   
        
        # Auxiliary attributes

        # Dictionary with the positions of the numbers
        # {number: (row, col)}
        self.positions = {}
        
        # List of empty positions
        # [(row, col)]
        self.empty_pos = []

        # List of used numbers
        # [number]
        used_numbers = []

        # Objective:
        # Find all missing numbers / Find all numbers position
        # Fill missing_numbers_neighbours
        for row in range(dim):
            for col in range(dim):
                number = board[row][col]
                # If position is empty
                if number == 0:
                    self.empty_pos.append((row, col))
                # If position is not empty
                else:
                    used_numbers.append(number)
                    self.positions[number] = (row, col)

        # List of missing numbers
        # [number]
        self.missing_numbers = self.get_number_choice_order(used_numbers)

    def get_board(self) -> list:
        return self.board

    def get_dim(self) -> int:
        return self.dim

    def get_positions(self) -> dict:
        return self.positions

    def get_empty_positions(self) -> list:
        return self.empty_pos

    def get_missing_numbers(self) -> list:
        return self.missing_numbers

    def get_number_of_empty_spaces(self) -> int:
        return len(self.missing_numbers)

    def get_number(self, row: int, col: int) -> int:
        return self.board[row][col]

    def get_number_choice_order(self, used_numbers):
        """ 
        Finds best missing numbers to place in the board.
        Only used to fill missing_number list in the constructor. 
        """
        used_numbers = sorted(used_numbers + [0, self.dim**2 + 1])
        order = []
        worse_used_numbers_dict = {}
        for i in range(len(used_numbers) - 1):
            number = used_numbers[i]
            difference = used_numbers[i+1] - number
            if difference == 2:
                order += list(range(number + 1, number + difference))
            if difference > 2:
                worse_used_numbers_dict[number] = difference
        final = []
        for number in worse_used_numbers_dict:
            if number == 0:
                final = list(range(number + worse_used_numbers_dict[number] - 1, number, -1))
            else:
                order += list(range(number + 1, number + worse_used_numbers_dict[number]))
        return order + final

    def get_number_seq(self, number: int) -> list:
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

    def get_empty_neighbours_positions(self, row: int, col: int) -> set:
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
        self.board[row][col] = number
        self.positions[number] = (row, col)
        self.empty_pos.remove((row, col))
        
    def get_best_positions(self, number, max_seq) -> list:

        # Create a set which is an intersection of all available positions for each number in max_seq
        # This positions are the only ones that can be used to place the number
        neighbours = self.get_empty_neighbours_positions(*self.positions[max_seq[0]])
        if(len(max_seq) == 2):
            neighbours = neighbours & self.get_empty_neighbours_positions(*self.positions[max_seq[1]])
            
        # Verify that for each available position, the distance to every number is valid
        positions = []
        for neighbour in neighbours:
            valid_neighbor = True
            for position in self.positions:
                # abs       -> distance in terms of integers            (e.g. 7-5 = 2)
                # manhattan -> distance in terms of moves in the board  (e.g. (3,1)-(2,2)=(1,1)=2)
                if abs(number-position) < manhattan_distance(self.positions[position], neighbour):
                    valid_neighbor = False
                    break
            if valid_neighbor:
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

    def check_valid(self, board, number, missing_numbers, row, col):
        for neighbour in board.get_neighbours(row, col):
            if neighbour != 0:
                neighbour_pos = board.positions[neighbour]
                if len(board.get_empty_neighbours_positions(*neighbour_pos)) == 1:
                    for number_seq in board.get_number_seq(neighbour) + [number]:
                        if number_seq in missing_numbers:
                            return False
        return True

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """

        board = state.board
        missing_numbers = board.get_missing_numbers()
        number = missing_numbers.pop(0)

        # List of possible sequence for number based on already placed numbers
        # [number-1,number+1] or [number-1] or [number+1]
        max_seq = [x for x in board.get_number_seq(number) if x not in missing_numbers]

        # List of actions based of available positions around each number of max_seq
        # Notice that number can only be place adjacent to one of the numbers in max_seq 
        return [(row, col, number) for (row, col) in board.get_best_positions(number, max_seq) 
                if self.check_valid(board, number, missing_numbers, row, col)]

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        new_state = deepcopy(state)
        new_state.board.add_number(action[0], action[1], action[2])
        return new_state

    def goal_test(self, state: NumbrixState):
        return state.board.get_number_of_empty_spaces() == 0

    def h(self, node: Node):
        board = node.state.board
        total = 0
        for space in board.get_empty_positions():
            total += (4-len(board.get_empty_neighbours_positions(*space)))**2
        return total


def main():
    # Lê tabuleiro do ficheiro
    board = Board.parse_instance(sys.argv[1])

    # Cria uma instancia de Numbrix
    problem = Numbrix(board)

    # Obtem o nó solução usando A*
    #goal_node = depth_first_tree_search(problem)
    goal_node = greedy_search(problem, problem.h) # 2 Memory Limit, 2 Time Limit
    #goal_node = astar_search(problem)  # 2 Memory Limit, 2 Time Limit
    #goal_node = recursive_best_first_search(problem)
    # Mostra tabuleiro final
    goal_node.state.board.print_board()


if __name__ == "__main__":
    main()