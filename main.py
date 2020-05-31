import numpy as np
import sys


def print_board(state):
    grid = state.grid

    print(grid)
    print(state.score)
    print('\n')
    for row in grid:
        for cell in row:
            if cell == 0:
                print(' * ', end='')
            elif cell == 1:
                print(' X ', end='')
            elif cell == -1:
                print(' O ', end='')
        print('\n')
    print('\n\n')


def minimax_decision(state):
    score = max_value(state)
    return state.search_action(score)


def max_value(state):
    if terminal(state):
        return state.score

    # largest negative int
    score = -sys.maxsize - 1

    for next_move in state.moves:
        score = max(score, min_value(next_move))
    return score


def min_value(state):
    if terminal(state):
        return state.score

    # larges positive int
    score = sys.maxsize

    for next_move in state.moves:
        score = min(score, max_value(next_move))
    return score


def terminal(state):
    return abs(state.score) == grid_size or len(state.moves) == 0


class State():
    def __init__(self, grid, empty_cells, player_score):
        self.grid = grid
        self.empty_cells = empty_cells
        self.player_score = player_score
        self.score = self.set_score()
        self.moves = self.successors()

    def search_action(self, value):
        for state in self.moves:
            if state.score == value:
                return state
        return False

    def set_score(self):
        scores = []
        scores.append(np.sum(grid, axis=0))
        scores.append(np.sum(grid, axis=1))
        scores.append([np.sum(np.diagonal(grid)),
                      np.sum(np.diagonal(np.fliplr(grid)))])

        s=0
        for axis in scores:
            max_v = max(axis)
            min_v = min(axis)
            
            if max_v > abs(min_v) and max_v > abs(s) : s = max(s, max_v)
            else : s = min(s, min_v)
        return s

    def successors(self):
        new_empty_cells = []
        new_grid = np.zeros((grid_size, grid_size))
        next_moves = []
        if np.sum(grid) > 0:
            player = -1
        else:
            player = 1
        for cell in self.empty_cells:
            
            row = cell[0]
            col = cell[1]

            new_grid[:] = self.grid
            new_grid[row, col] = player
            new_empty_cells[:] = self.empty_cells
            new_empty_cells.remove([row, col])
            new_state = State(new_grid, new_empty_cells, player)
            next_moves.append(new_state)

        return next_moves


def new_moves(state):
    return len(state.moves) != 0


def update_scores(row, col, player_score):
    row_scores[line] += player_score
    column_scores[col] += player_score

    # in main diagonal
    if row == col:
        diagonal_scores[0] += player_score

    # in secondary diagonal
    if row == grid_size-col-1:
        diagonal_scores[1] += player_score

    # check if it's a winning move
    if abs(row_scores[line]) == grid_size or abs(column_scores[col]) == grid_size or grid_size in abs(diagonal_scores):
        return True

    else:
        return False


def populate_empty_cells():
    for row in range(grid_size):
        for col in range(grid_size):
            current_state.empty_cells.append([row, col])


grid_size = 3
grid = np.zeros((grid_size, grid_size))
row_scores = np.zeros(grid_size)
column_scores = np.zeros(grid_size)
diagonal_scores = np.zeros(2)
current_state = State(grid, [], 1)
human_playing = False

populate_empty_cells()

while True:
    print_board(current_state)
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
        print('My turn! let me think...')
        player_score = 1
        current_state = minimax_decision(current_state)

    if not new_moves(current_state) or terminal(current_state):
        break

print_board(current_state)
 
if not new_moves(current_state):
    print('No more moves.')
else:
    if(human_playing):
        print('You won!')
    else:
        print('You lost!')

    # current_state = State(grid, new_empty_cells )
    # minimax_decision(current_state)
