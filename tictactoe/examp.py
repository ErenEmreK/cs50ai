from tictactoe import player, result, actions, minimax, utility, terminal, winner, find_best_move
import copy
X = "X"
O = "O"
EMPTY = None

board = [[X, EMPTY, X],
        [X, EMPTY, O],
        [EMPTY, O, O]]


def minimax(board):
    
    if terminal(board):
        return utility(board)
    
    if player(board) == X:
            
        v = -float("inf")       
        for action in actions(board):
            score = minimax(result(board, action))
            v = max(v, score)
            
        return v
    
    else:
        
        v = float("inf")
        for action in actions(board):
            score = minimax(result(board, action))
            v = min(v, score)
            
        return v
    
def find_best_action(board):
    
    best_action = (-1, -1)
    
    if player(board) == X:
        
        best_score = -float("inf")
        for action in actions(board):
            v = minimax(result(board, action)) 
            if v > best_score: best_action = action 
    
        return best_action
    
    else:
        
        best_score = float("inf")
        for action in actions(board):
            v = minimax(result(board, action))
            if v < best_score: best_action = action
            
        return best_action        
                
print(find_best_action(board))