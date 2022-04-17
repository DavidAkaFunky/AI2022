import sys

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

        # List of missing numbers
        # [number]
        self.missing_numbers = []

        # Dictionary with the status of each neighbor of missing number (True -> present, False -> missing)
        # {number: (isLeftNeighhorPresent, isRightNeighborPresent)}
        missing_numbers_neighbours = {x: [False, False] for x in range(1, self.dim ** 2 + 1)}
        missing_numbers_neighbours[1][0] = True
        missing_numbers_neighbours[dim**2][1] = True

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
                    self.update_missing_numbers_neighbours(missing_numbers_neighbours, number)
                    self.positions[number] = (row, col)

        # Objective:
        # Fill missing_numbers sorted by best number to place in the board first
        # This is done by simulating the placement of each number in the board
        while missing_numbers_neighbours != {}:
            best = self.get_best_missing_numbers(missing_numbers_neighbours)
            self.missing_numbers += best
            for number in best:
                self.update_missing_numbers_neighbours(missing_numbers_neighbours, number) 
          

    def update_missing_numbers_neighbours(self, missing_numbers_neighbours, number):
        missing_numbers_neighbours.pop(number)
        for (value, index) in ((number-1, 1), (number+1, 0)):
            try:
                missing_numbers_neighbours[value][index] = True
            except KeyError:
                pass
        
    def get_best_missing_numbers(self, missing_numbers_neighbours):
        """ 
        Finds best missing numbers to place in the board.
        Only used to fill missing_number list in the constructor. 
        """
        best_numbers = []
        alt_left = alt_right = 0
        # For each missing number
        for number in missing_numbers_neighbours:
            left = missing_numbers_neighbours[number][0]
            right = missing_numbers_neighbours[number][1]
            # If left and right neighbors are present add to best numbers
            if left and right:
                best_numbers.append(number)
            # Keep track of alternative numbers in case no number has both neighbors present
            if number != 1 and number != self.dim**2:
                if alt_left == 0 and left:
                    alt_left = number
                if alt_right == 0 and right:
                    alt_right = number
        # If there is no number with both neighbours present
        if best_numbers == []:
            # Add smallest number that has at least one neighbor present
            # Give priority to number with left neighbor
            best_numbers.append(alt_left) if alt_left != 0 else best_numbers.append(alt_right)

        return best_numbers

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

def main():
    # Lê tabuleiro do ficheiro
    for _ in range(10000):
        board = Board.parse_instance(sys.argv[1])


if __name__ == "__main__":
    main()