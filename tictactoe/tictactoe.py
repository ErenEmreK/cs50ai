"""
Tic Tac Toe Player
"""
import random
import math
import copy

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

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    counter_x = counter_o = 0
    
    for row in board:
        for column in row:
            if column == X:
                counter_x += 1
            if column == O:
                counter_o += 1
    
    if counter_o < counter_x:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = set()
    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                action_set.add((row, column))
    
    return action_set

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """    
    copied_board = copy.deepcopy(board)
    #print((copied_board))
    #print((action))
    try:
        copied_board[action[0]][action[1]]  = player(board)
        return copied_board
    
    except copied_board[action[0]][action[1]] != EMPTY:
        raise "Not a valid action."
        
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if (
        board[0][0] == board[1][1] == board[2][2] or
        board[0][2] == board[1][1] == board[2][0]
        ):
        return board[1][1]
    
    for row in range(len(board)):
        if board[row][0] == board[row][1] == board[row][2]:
            return board[row][0]
        elif board[0][row] == board[1][row] == board[2][row]:
            return board[0][row]
    
    return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board) != None) or ((EMPTY not in board[0]) and
    (EMPTY not in board[1]) and (EMPTY not in board[2])):
        return True  
       
    return False 

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    return 0


def minVal_maxVal(board):
    """
    Actual MiniMax algorithm that returns the output value for an action
    """
    
    if terminal(board):
        return utility(board)
    
    if player(board) == X:
            
        v = -float("inf")       
        for action in actions(board):
            score = minVal_maxVal(result(board, action))
            if score == 1: return score
            v = max(v, score)
            
        return v
    
    else:
        
        v = float("inf")
        for action in actions(board):
            score = minVal_maxVal(result(board, action))
            if score == -1: return score
            v = min(v, score)
            
        return v
    
def minimax(board):
    """
    Uses minimax algorithm to find best move for the board
    (Names got a bit confusing since i wanted staff to 
    not to deal with different function names)
    """
    best_action = (-1, -1)
    
    if player(board) == X:
        
        best_score = -float("inf")
        for action in actions(board):
            v = minVal_maxVal(result(board, action))
            if v == 1: return action 
            if v > best_score: 
                best_score = v
                best_action = action 
    
        return best_action
    
    else:
        
        best_score = float("inf")
        for action in actions(board):
            v = minVal_maxVal(result(board, action))
            if v == -1: return action
            if v < best_score: 
                best_score = v
                best_action = action
            
        return best_action        
                
