import sys
import numpy as np
from numpy.core.numeric import zeros_like

class Board:
    def __init__(self, board, id) -> None:
        self.id = id
        self.completed = False
        self.board = np.array(board)
        # keep track of calls in a separate board,
        # initialized to all zeros
        self.called_board = zeros_like(self.board)

    def __repr__(self) -> str:
        return str(self.called_board)

    def draw_number(self, number) -> bool:
        drawn_index = np.where(self.board == number)
        if len(drawn_index[0]) == 0:
            return False
        # I'll assume each board only has one or zero
        # matching numbers.
        self.called_board[drawn_index[0][0], drawn_index[1][0]] = 1
        return self.check_if_won()

    def check_if_won(self) -> bool:
        # Check if any of the rows or columns are all 1
        for axis in (0,1):
            winning_board = np.apply_along_axis(
                lambda x: all(x == 1),
                axis,
                self.called_board
            )
            if any(winning_board):
                return True
        return False

    def score_board(self, number) -> int:
        return np.sum(
            self.board[self.called_board != 1] * number
            )

# Read in numbers and boards:

boards = []

with open(sys.argv[1], 'r') as f:
    # kinda gross way to take the first line and convert
    # it all to integers
    nums = [int(x) for x in f.readline().rstrip().split(',')]
    
    # skip the blank line after the numbers
    f.readline()

    # iterate through the remaining lines, making lists of
    # lists and converting them to a Board at every newline
    working_board = []
    id_num = 1
    for line in f:
        if line == '\n':
            boards.append(Board(working_board, id_num))
            id_num += 1
            working_board = []
            continue

        working_board.append(
            [int(x) for x in line.rstrip().split()]
        )

    # python doesn't read in the final newline, so you
    # have to add the final working_board manually
    boards.append(Board(working_board, id_num))

# the word "board" looks meaningless to me now

# part one
def play_bingo(boards, draws):
    for num in draws:
        for board in boards:
            if board.draw_number(num):
                return board.score_board(num)

print(play_bingo(boards, nums))

# part two
def lose_bingo(boards, draws):
    for num in draws:
        for board in boards:
            if board.completed:
                continue
            if board.draw_number(num):
                if len(boards) > 1:
                    board.completed = True
                else:
                    return board.score_board(num)
        boards = [x for x in boards if not x.completed]

print(lose_bingo(boards, nums))
