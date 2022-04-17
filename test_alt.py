import sys

class Board:
       
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