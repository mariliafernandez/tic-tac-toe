import numpy as np
import sys
from Tkinter import *


grid_size = 3
grid = np.zeros((grid_size, grid_size))
row_scores = np.zeros(grid_size)
column_scores = np.zeros(grid_size)
diagonal_scores = np.zeros(2)
human_playing = False


# def print_board(state):
#     print(state.grid)
#     print(state.score)
#     print('\n')
#     for row in state.grid:
#         for cell in row:
#             if cell == 0:
#                 print(' * ', end='')
#             elif cell == 1:
#                 print(' X ', end='')
#             elif cell == -1:
#                 print(' O ', end='')
#         print('\n')
#     print('\n\n')


def minimax_decision(state):
    new_state = max_value(state)
    # next_state=State(state.grid, state.empty_cells, state.player_score)
    return new_state
     
def max_value(state):
    max_state = State(state.grid, state.empty_cells, state.player_score)

    if terminal(state):
        return state

    # largest negative int
    score = -sys.maxsize - 1
    
    state.moves = state.successors()
    for move in state.moves:
        if score > min_value(move).score:
            max_state = State(move.grid, move.empty_cells, -move.player_score)
            score = max_state.score
        # score = max(score, min_value(move))
    return max_state


def min_value(state):
    min_state = State(state.grid, state.empty_cells, state.player_score)
    
    if terminal(state):
        return state

    # larges positive int
    score = sys.maxsize

    state.moves = state.successors()

    for move in state.moves:
        if score < max_value(move).score:
            min_state = State(move.grid, move.empty_cells, -move.player_score)
            score = min_state.score
        # score = min(score, max_value(next_move))
    return min_state


def terminal(state):
    print('empty cells: ', len(state.empty_cells))
    print('size: ', grid_size)
    return abs(state.score) == grid_size or len(state.empty_cells) == 0


class State():
    def __init__(self, grid, empty_cells, player_score):
        self.grid = grid
        self.empty_cells = empty_cells
        self.player_score = player_score
        self.score = self.set_score()
        self.moves = []
        # self.moves = self.successors()

    def set_score(self):
        score_v = 0
        scores = []
        scores.append(np.sum(grid, axis=0))
        scores.append(np.sum(grid, axis=1))
        scores.append([np.sum(np.diagonal(grid)),
                      np.sum(np.diagonal(np.fliplr(grid)))])

        for axis in scores:
            max_v = max(axis)
            min_v = min(axis)
            if min_v == -grid_size : score_v = -3
            if max_v == grid_size : score_v = 3
            else: score_v = 0
            # elif max_v > abs(min_v) and max_v > abs(score_v) : score_v = 1
            # max(max_v, score_v)
            # elif abs(min_v) > max_v and abs(min_v) > abs(score_v) : score_v = -1
            # min(min_v, score_v)
        return score_v


    def successors(self):
        new_empty_cells = []
        next_moves = []

        # if np.sum(grid) > 0 : player = -1
        # else : player = 1

        player = -self.player_score

        # print('\nempty cells')
        # print(self.empty_cells)
        for cell in self.empty_cells:
            row = cell[0]
            col = cell[1]

            new_grid = np.zeros((grid_size, grid_size))
            new_grid[:] = self.grid
            new_grid[row, col] = player
            new_empty_cells[:] = self.empty_cells
            new_empty_cells.remove([row, col])
            new_state = State(new_grid, new_empty_cells, player)
            next_moves.append(new_state)

        return next_moves


def new_moves(state):
    return len(state.empty_cells) != 0

def populate_empty_cells(grid_size):
    for row in range(grid_size):
        for col in range(grid_size):
            current_state.empty_cells.append([row, col])



current_state = State(grid, [], 1)

populate_empty_cells(grid_size)
app.go()


while True:
    print(current_state.grid)

    human_playing = not human_playing
    empty_cells = current_state.empty_cells
    grid = current_state.grid

    if(human_playing):
        print('\nYour turn! choose wisely!\n')
        player_score = -1
        while True:
            input_text = '\nEnter line[0-'+str(grid_size-1)+']: '
            line = int(input(input_text))
            input_text = '\nEnter column[0-'+str(grid_size-1)+']: '
            column = int(input(input_text))
            if [line, column] in empty_cells:
                empty_cells.remove([line, column])
                grid[line, column] = player_score
                current_state = State(grid, empty_cells, player_score)
                break
            else:
                print('\nInvalid move, choose again.')

    else:
        print('\n\nMy turn! let me think...\n')
        player_score = 1
        current_state = minimax_decision(current_state)

    current_state.moves = current_state.successors()
    if not new_moves(current_state) or terminal(current_state):
        break

print(current_state.grid)

 
if not new_moves(current_state):
    print('No more moves.')
else:
    if(human_playing):
        print('You won!')
    else:
        print('You lost!')