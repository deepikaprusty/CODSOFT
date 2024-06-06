import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# Helper functions
def get_diagonal(board):
    return [[board[0][0], board[1][1], board[2][2]],
            [board[0][2], board[1][1], board[2][0]]]

def get_columns(board):
    columns = []
    for i in range(3):
        columns.append([row[i] for row in board])
    return columns

def three_in_a_row(row):
    return row[0] is not None and row.count(row[0]) == 3

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)
    return O if count_x > count_o else X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                action.add((i, j))
    return action

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] is not EMPTY:
        raise Exception("Invalid move")
    
    next_move = player(board)
    new_board = deepcopy(board)
    new_board[i][j] = next_move
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lines = board + get_columns(board) + get_diagonal(board)
    for line in lines:
        if three_in_a_row(line):
            return line[0]
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(all(cell is not EMPTY for cell in row) for row in board)

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def max_alpha_beta_pruning(board, alpha, beta):
    if terminal(board):
        return utility(board), None
    max_val = float("-inf")
    best_action = None
    for action in actions(board):
        min_val = min_alpha_beta_pruning(result(board, action), alpha, beta)[0]
        if min_val > max_val:
            best_action = action
            max_val = min_val
        alpha = max(alpha, max_val)
        if beta <= alpha:
            break
    return max_val, best_action

def min_alpha_beta_pruning(board, alpha, beta):
    if terminal(board):
        return utility(board), None
    min_val = float("inf")
    best_action = None
    for action in actions(board):
        max_val = max_alpha_beta_pruning(result(board, action), alpha, beta)[0]
        if max_val < min_val:
            best_action = action
            min_val = max_val
        beta = min(beta, min_val)
        if beta <= alpha:
            break
    return min_val, best_action

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    current_player = player(board)
    if current_player == X:
        return max_alpha_beta_pruning(board, float("-inf"), float("inf"))[1]
    else:
        return min_alpha_beta_pruning(board, float("-inf"), float("inf"))[1]
