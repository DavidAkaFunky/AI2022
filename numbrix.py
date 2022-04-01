# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 03:
# 95550 David Belchior
# 95562 Diogo Santos

import sys
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search


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
        self._board = board
        self._dim = dim


    def get_board(self) -> list:
        return self._board


    def get_dim(self) -> int:
        return self._dim


    def get_number(self, row: int, col: int) -> int:

        """ Devolve o valor na respetiva posição do tabuleiro. """

        return self._board[row][col]

    
    def get_numbers(self):
        
        """ Devolve uma lista com todos os valores do tabuleiro. """

        return [number for row in self._board for number in row]


    def get_missing_numbers(self):
            
        """ Devolve uma lista com todos os valores que faltam no tabuleiro. """

        return [number for number in range(1, self._dim**2+1) if number not in self.get_numbers()]	


    def get_number_seq(self, number: int) -> tuple:

        """ Devolve uma lista com todos os valores imediatamente adjacentes ao numero. """

        res = ()
        if number > 1:
            res += (number-1,)
        if number < self._dim**2:
            res += (number+1,)
        return res


    def is_valid_neighbour(self, row: int, col: int, number: int):

        """ Verifica se o numero é um vizinho valido para a respetiva posicao."""

        validNeighbours = []
        # Para valor vizinho
        for neighbour in self.get_neighbours(row, col):
            # Adiciona valores adjacentes
            validNeighbours += self.get_number_seq(neighbour)

        # é um valor valido se pertencer à lista de valores adjacentes
        return number in validNeighbours


    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):

        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """

        numbers = ()
        for x in (row-1, row+1):
            if x < 0 or x >= self._dim:
                numbers += (None,)
            else:
                numbers += (self.get_number(x, col),)
        return numbers

    
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):

        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """

        numbers = ()
        for y in (col-1, col+1):
            if y < 0 or y >= self._dim:
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
            if y >= 0 and y < self._dim and self.get_number(row, y) == 0:
                available_positions += ((row,y),)
        for x in (row-1, row+1):
            if x >= 0 and x < self._dim and self.get_number(x, col) == 0:
                available_positions += ((x,col),)

        return available_positions

    
    def get_actions(self, row: int, col: int):

        """ Devolve uma lista de acoes possiveis de realizar na resptiva posicao. """

        actions = []
        for number in self.get_missing_numbers():
            if self.is_valid_neighbour(row, col, number):
                actions.append((row,col,number))

        return actions

    
    def add_number(self, row: int, col: int, number: int) -> None:

        """ Atualiza o valor na respetiva posicao do tabuleiro ."""

        self._board[row][col] = number


    def print_board(self):

        """ Imprime o tabuleiro na consola. """

        for row in self._board:
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

        # Available actions
        total_actions = ()
        # For each position
        for row in range(state.board.get_dim()):
            for col in range(state.board.get_dim()):
                # If position is empty
                if state.board.get_number(row, col) == 0:
                    # Get all available actions
                    actions = state.board.get_actions(row, col)
                    for action in actions:
                        total_actions += (action,)
                
        return total_actions


    def result(self, state: NumbrixState, action):

        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """

        state.board.add_number(action[0],action[1],action[2])


    def goal_test(self, state: NumbrixState):

        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """

        board = state.board
        dim = board.get_dim()

        for row in range(dim):
            for col in range(dim):
                neighbours = board.get_neighbours(row, col)
                number_seq = board.get_number_seq(board.get_number(row, col))
                for number in number_seq:
                    if number not in neighbours:
                        return False 
      
        return True
        

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        return 0
    

if __name__ == "__main__":

    # Lê tabuleiro do ficheiro
    board = Board.parse_instance(sys.argv[1])

    # Cria uma instancia de Numbrix
    problem = Numbrix(board)

    board.print_board()
    
    # Obtem o nó solução usando A*
    goal_node = astar_search(problem)

    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board.to_string(), sep="") 