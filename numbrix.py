# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 03:
# 95550 David Belchior
# 95562 Diogo Santos

from dis import findlabels
import sys

import pickle
from search import Problem, Node, depth_first_tree_search, greedy_search, astar_search
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
        self.create_number_seq()
        self.create_neighbours_positions()
        
        # List of empty positions
        # [(row, col)]
        self.empty_pos = []

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
                    self.positions[number] = (row, col)

        # List of missing numbers
        # [number]
        self.missing_numbers = self.get_number_choice_order(list(self.positions.keys()))

    def get_number_choice_order(self, used_numbers):
        """ 
        Finds best missing numbers to place in the board.
        Only used to fill missing_number list in the constructor. 
        """
        used_numbers = sorted(used_numbers + [0, self.dim**2 + 1])
        first = []
        next = []
        worse_used_numbers_dict = {}
        for i in range(len(used_numbers) - 1):
            number = used_numbers[i]
            difference = used_numbers[i+1] - number
            if difference == 2:
                if number == 0 or number == self.dim**2-1 or len([pos for pos in self.get_empty_neighbours_positions(*self.positions[number]) if pos in set(self.get_empty_neighbours_positions(*self.positions[number + 2]))]) == 1:
                    first.append(number + 1)
                else:
                    next.append(number + 1)
            if difference > 2:
                worse_used_numbers_dict[number] = difference
        worse_used_numbers_dict = dict(sorted(worse_used_numbers_dict.items(), key=lambda x:x[1]))
        final = []
        for number in worse_used_numbers_dict:
            if number == 0:
                final += list(range(number + worse_used_numbers_dict[number] - 1, number, -1))
            else:
                first += list(range(number + 1, number + worse_used_numbers_dict[number]))
        return first + next + final

    def create_number_seq(self):
        """ Devolve uma lista com todos os valores imediatamente adjacentes ao numero. """
        for number in range(1, self.dim ** 2 + 1):
            res = []
            if number > 1:
                res.append(number - 1)
            if number < self.dim ** 2:
                res.append(number + 1)
            number_seqs[number] = res

    def get_neighbours(self, row: int, col: int):
        """ Devolve os valores vizinhos da respetiva posição. """

        return [self.board[y][x] for (y, x) in neighbours_positions[(row, col)]]

    def create_neighbours_positions(self) -> list:
        """ Devolve as posicoes que estao em redor da respetiva posicao. """
        for row in range(self.dim):
            for col in range(self.dim):
                available_positions = []
                for y in (col - 1, col + 1):
                    if 0 <= y < self.dim:
                        available_positions.append((row, y))
                for x in (row - 1, row + 1):
                    if 0 <= x < self.dim:
                        available_positions.append((x, col))
                neighbours_positions[(row, col)] = available_positions
        
    def get_empty_neighbours_positions(self, row: int, col: int) -> list:
        """ Devolve as posicoes que estao por preencher em redor
        da respetiva posicao. """

        return [(y, x) for (y, x) in neighbours_positions[(row, col)] if self.board[y][x] == 0]

    def get_filled_neighbours_positions(self, row: int, col: int) -> list:
        """ Devolve as posicoes que estao preenchidas em redor
        da respetiva posicao. """

        return [(y, x) for (y, x) in neighbours_positions[(row, col)] if self.board[y][x] != 0]

    def add_number(self, row: int, col: int, number: int) -> None:
        """ Atualiza o valor na respetiva posicao do tabuleiro ."""
        self.board[row][col] = number
        self.positions[number] = (row, col)
        self.empty_pos.remove((row, col))
        
    def manhattan_condition(self, number, neighbour) -> bool:
        """
        Verify if number is a valid distance from every other number in the board.
        """
        for position in self.positions:
            # abs       -> distance in terms of integers            (e.g. 7-5 = 2)
            # manhattan -> distance in terms of moves in the board  (e.g. (3,1)-(2,2)=(1,1)=2)
            if abs(number-position) < manhattan_distance(self.positions[position], neighbour):
                return False
        return True
    
    def locked_condition(self, number, position) -> bool:
        """
        Verify if number's neighbours don't get locked
        e.g 1   2   3 , 7 would be "locked" 
            4   7   9
        """
        for (row, col) in neighbours_positions[position]:
            neighbour_number = self.board[row][col]
            if len(self.get_empty_neighbours_positions(row, col)) == 1:
                if neighbour_number != 0:                
                    for number_seq in number_seqs[neighbour_number] + [number]:
                        if number_seq in self.missing_numbers:
                            return False
                else:
                    neighbour_neighbours = sorted(self.get_neighbours(row, col) + [0, number, self.dim**2 + 1])
                    has_seq = False
                    for i in range(len(neighbour_neighbours)-1):
                        number_neighbour = neighbour_neighbours[i]
                        if neighbour_neighbours[i+1] - number_neighbour == 2 and number_neighbour+1 in self.missing_numbers:
                            has_seq = True
                            break
                    if not has_seq:
                        return False
            
        return True

    def print_board(self):
        """ Imprime o tabuleiro na consola. """
        for row in self.board:
            print("\t".join(str(number) for number in row))

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

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """

        board = state.board
        missing_numbers = board.missing_numbers
        choice = missing_numbers[0]
        max_seq = [x for x in number_seqs[choice] if x not in missing_numbers]
        choice_possible_positions = board.get_empty_neighbours_positions(*board.positions[max_seq[0]])
        chosen = False
        if len(max_seq) == 2:
            choice_possible_positions = [pos for pos in choice_possible_positions if pos in set(board.get_empty_neighbours_positions(*board.positions[max_seq[1]]))]
        if len(choice_possible_positions) == 1:
            chosen = True
        if not chosen:
            for number in missing_numbers[1:]:    
            
                # List of possible sequence for number based on already placed numbers
                # [number-1,number+1] or [number-1] or [number+1]
                max_seq = [x for x in number_seqs[number] if x not in missing_numbers]
                if len(max_seq) == 0:
                    continue

                # Create a set which is an intersection of all available positions for each number in max_seq
                # This positions are the only ones that can be used to place the number
                possible_positions = board.get_empty_neighbours_positions(*board.positions[max_seq[0]])
                if len(max_seq) == 2:
                    possible_positions = [pos for pos in possible_positions if pos in set(board.get_empty_neighbours_positions(*board.positions[max_seq[1]]))]
                if len(possible_positions) == 1:
                    choice = number
                    choice_possible_positions = possible_positions
                    break

        missing_numbers.remove(choice)

        # List of actions based of available positions around each number of max_seq
        # Notice that number can only be place adjacent to one of the numbers in max_seq 
        return [(*x, choice) for x in choice_possible_positions if board.locked_condition(choice, x)]

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        new_state = pickle.loads(pickle.dumps(state, -1))
        new_state.board.add_number(*action)
        return new_state

    def goal_test(self, state: NumbrixState):
        return len(state.board.missing_numbers) == 0

    def h(self, node: Node):
        board = node.state.board
        total = 0
        empty_positions = board.empty_pos
        for space in empty_positions:
            total += (len(board.get_filled_neighbours_positions(*space)))**2
        return total


def main():
    # Lê tabuleiro do ficheiro
    board = Board.parse_instance(sys.argv[1])

    # Cria uma instancia de Numbrix
    problem = Numbrix(board)

    # Obtem o nó solução usando A*
    goal_node = depth_first_tree_search(problem) # 2 Time Limit
    #goal_node = greedy_search(problem, problem.h) # 
    #goal_node = astar_search(problem)  # 
    #goal_node = recursive_best_first_search(problem)
    # Mostra tabuleiro final
    goal_node.state.board.print_board()


if __name__ == "__main__":
    neighbours_positions = {}
    number_seqs = {}
    main()