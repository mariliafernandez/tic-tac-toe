import numpy as np

def print_board():
    print('\n')
    print(grid)
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

# def max_value(state):
#     # if terminal_test(state):
#         return state.utility

#     # largest negative int 
#     score = -sys.maxint - 1

#     for s in state.successors:
#         score = max(u, min_value(s))
#     return score

# def min_value(state):
#     if terminal_test(state):
#         return state.utility

#     # larges positive int
#     score = sys.maxint()

#     for s in state.successors():
#         score = min(u, max_value(s))
#         action = s
#     return score


class State():
    def __init__(self, grid, empty_cells):
        self.grid = grid
        self.utility = self.set_utility()
        self.successors_list = self.successors()
        self.empty_cells = empty_cells

    def search_action(self, u):
        for s in self.successors_list:
            if self.utility == u:
                return s
        return False

    def set_utility(self):
        row_occurrences_x = []
        column_occurrences_x = []
        diagonal_occurrences_x = []
        row_occurrences_o = []
        column_occurrences_o = []
        diagonal_occurrences_o = []


        for i in range(grid_size):
            row_occurrences_x.append(sum(grid[i,:] == x_score))
            column_occurrences_x.append(sum(grid[:,i] == x_score))
            diagonal_occurrences_x.append(np.count_nonzero(self.grid.diagonal() == b'X', axis=0))

            row_occurrences_o.append(sum(self.grid[i,:] == o_score))
            column_occurrences_o.append(np.count_nonzero(self.grid == b'O', axis = 0))
            diagonal_occurrences_o.append(np.count_nonzero(self.grid.diagonal() == b'O', axis=0))

        if 3 in row_occurrences_x or 3 in column_occurrences_x or 3 in diagonal_occurrences_x:
            return 1
        elif 3 in row_occurrences_o:
            return -1
        else:
            return 0
        
     
    def successors(self):
        self.successors_list = []
        for i in range(len(empty_cells)):
            line = empty_cells[i][0]
            column = empty_cells[i][1]

            new_grid = grid
            new_grid[line, column]  = 'a'
            new_empty_cells = empty_cells
            new_state = State(new_grid, new_empty_cells.remove([empty_cells[i][0], empty_cells[i][1]]))
            self.successors_list.append(new_state)
        return self.successors_list

def new_moves():
    return not empty_cells == []

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

    else : return False


def populate_empty_cells():
    for row in range(grid_size):
        for col in range(grid_size):
            empty_cells.append([row, col])


grid_size = 3
grid = np.zeros((grid_size,grid_size))
row_scores = np.zeros(grid_size)
column_scores = np.zeros(grid_size)
diagonal_scores = np.zeros(2)
human_playing = False
empty_cells = []

populate_empty_cells()

while True:
    print_board()
    human_playing = not human_playing

    if(human_playing):
        print('\nYour turn! choose wisely!\n')
        player_score=1
        while True:
            input_text='\nEnter line[0-'+str(grid_size-1)+']: '
            line = int(input(input_text))
            input_text='\nEnter column[0-'+str(grid_size-1)+']: '
            column = int(input(input_text))
            if [line, column] in empty_cells:
                empty_cells.remove([line, column])
                break
            else:
                print('\nInvalid move, choose again.')
        
    else:
        print('Computer turn! thinking...!')
        player_score=-1
        target = empty_cells.pop()
        line = target[0]
        column = target[1]
        print('\n['+ str(line) + ',' + str(column)  +']:')
    
    grid[line, column] = player_score
    winner = update_scores(line, column, player_score)

    if not new_moves() or winner: break

print_board()

if winner:
    if(human_playing):
        print('You won!')
    else:
        print('You lost!')
elif not new_moves():
    print('No more moves.')

else:
    print('qq ta conteseno')

    # current_state = State(grid, new_empty_cells )
    # minimax_decision(current_state)