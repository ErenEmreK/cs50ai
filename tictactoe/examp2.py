from tictactoe import player, result, actions, minimax, utility, terminal, winner, find_best_move
import copy 
X = "X"
O = "O"
EMPTY = None

board = [[X, O, X],
        [EMPTY, O, O],
        [EMPTY, EMPTY, X]]


print(board)
 
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """    
    copied_board = copy.deepcopy(board)
    try:
        copied_board[action[0]][action[1]]  = player(board)
        return copied_board
    
    except copied_board[action[0]][action[1]] != EMPTY:
        raise "Not a valid action."
        
new = result(board, list(actions(board))[1])

print(new)
print(board)

"""LOOK İNTO PLAYER FUNCTİON"""