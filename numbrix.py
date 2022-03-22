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
        
    # TODO: outros metodos da classe

    def get_board(self):
        return self.board


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

    def get_number_seq(self, number: int) -> tuple:
        res = ()
        if number > 1:
            res += (number-1,)
        if number < self._dim**2:
            res += (number+1,)
        return res
    
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
        neighbours = self.adjacent_vertical_numbers(row, col) + self.adjacent_horizontal_numbers(row, col)
        return tuple(filter(lambda n: n != None, neighbours))
    
    def add_number(self, number: int, row: int, col: int) -> None:
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



    # TODO:outros metodos da classe


class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.board = board
        pass

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        # action -> tuplo (2,1,8) -> “preenchero número 8 na posição linha 2 coluna 1
        # TODO
        pass

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        # dada uma acao e um estado retorna o resultado de aplicar essa acao a esse estado
        # TODO
        state.get_board().add_number(action[0],action[1],action[2])
        pass

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
        # estado atual -> node.state
        # TODO
        pass
    
    # TODO: outros metodos da classe

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance(sys.argv[1])
    board.print_board()
    problem = Numbrix(board)
    initial_state = NumbrixState(board)

    print("Is goal?", problem.goal_test(initial_state))
    n = board.get_dim()
