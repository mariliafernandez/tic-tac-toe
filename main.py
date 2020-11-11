import numpy as np
import sys
from Tkinter import *

GRID_SIZE = 3
grid = np.zeros((GRID_SIZE, GRID_SIZE))
row_scores = np.zeros(GRID_SIZE)
column_scores = np.zeros(GRID_SIZE)
diagonal_scores = np.zeros(2)
human_playing = False
print(grid)
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
    
    moves = state.successors()
    for move in moves:
        print(move.grid)
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

    moves = state.successors()

    for move in moves:
        print(move.grid)

        if score < max_value(move).score:
            min_state = State(move.grid, move.empty_cells, -move.player_score)
            score = min_state.score
        # score = min(score, max_value(next_move))
    return min_state

def terminal(state):
    return abs(state.score) == GRID_SIZE

def human_win(state):
    return state.score == -GRID_SIZE 

def robot_win(state):
    return state.score == GRID_SIZE

def new_moves(state):
    return len(state.empty_cells) > 0

def populate_empty_cells(GRID_SIZE):
    empty_cells = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            empty_cells.append([row, col])
    return empty_cells

class State():
    def __init__(self, grid, empty_cells, player_score):
        self.grid = grid
        self.empty_cells = empty_cells
        self.player_score = player_score
        self.score = self.score()

    def score(self):
        score = 0
        scores = []
        scores.append(np.sum(grid, axis=0))
        scores.append(np.sum(grid, axis=1))
        scores.append([np.sum(np.diagonal(grid)),
                      np.sum(np.diagonal(np.fliplr(grid)))])

        for axis in scores:
            max_v = max(axis)
            min_v = min(axis)
            if min_v == - GRID_SIZE : score = -3
            elif max_v == GRID_SIZE : score = 3
            elif max_v > abs(min_v) and max_v > abs(score) : score = 1
            elif abs(min_v) > max_v and abs(min_v) > abs(score) : score = -1
            else: score = 0
            # min(min_v, this.score)
        return score


    def successors(self):
        empty_cells = []
        next_moves = []

        # print('\nempty cells')
        # print(self.empty_cells)
        for cell in self.empty_cells:
            row = cell[0]
            col = cell[1]

            new_grid = np.zeros((GRID_SIZE, GRID_SIZE))
            new_grid[:] = self.grid
            new_grid[row, col] = -self.player_score
            empty_cells[:] = self.empty_cells
            empty_cells.remove([row, col])
            successor = State(new_grid, empty_cells, -self.player_score)
            next_moves.append(successor)

        return next_moves


def main():

    global grid, human_playing
    empty_cells = populate_empty_cells(GRID_SIZE) 
    current_state = State(grid, empty_cells, 1)
    # app.go()
    print(current_state.grid)


    while True:
        human_playing = not human_playing
        empty_cells = current_state.empty_cells
        grid = current_state.grid

        if(human_playing):
            print('\nYour turn! choose wisely!\n')
            print(current_state.grid)

            while True:
                input_text = '\nEnter line[0-'+str(GRID_SIZE-1)+']: '
                line = int(input(input_text))
                input_text = '\nEnter column[0-'+str(GRID_SIZE-1)+']: '
                column = int(input(input_text))
                if [line, column] in empty_cells:
                    empty_cells.remove([line, column])
                    grid[line, column] = -1
                    current_state = State(grid, empty_cells, -1)
                    break
                else:
                    print('\nInvalid move, choose again.')

        else:
            print()
            print(current_state.grid)
            print('\n\nMy turn! let me think...\n')
            current_state = minimax_decision(current_state)

        moves = current_state.successors()


        
        if not new_moves(current_state):
            print('No more moves.')
        elif human_win(current_state):
            print('You won!')
        elif robot_win(current_state):
            print('You lost!')

if __name__ == '__main__':
    main()