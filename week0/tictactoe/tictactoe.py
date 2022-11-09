"""
Tic Tac Toe Player
"""
import copy
import math

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
    initial_board = initial_state()
    if board == initial_board:
        return X
    elif terminal(board):
        return None
    else:
        number_x = 0
        number_o = 0
        for row in board:
            for point in row:
                if point == X:
                    number_x +=1
                elif point == O:
                    number_o +=1
        if number_x > number_o:
            return O
        else:
            return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        return None
    else:
        actions = set()
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == EMPTY:
                    actions.add((i,j))
        return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    deep_copy = copy.deepcopy(board)
    if action not in actions(board):
        raise Exception("Not valid move")
    else:
        if player(board) == X:
            deep_copy[action[0]][action[1]] = X
        elif player(board) == O:
            deep_copy[action[0]][action[1]] = O
        return deep_copy 

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def check_row(board1,player1):
        for i in range(len(board1)):
            count =0
            for j in range(len(board1)):
                if board1[i][j] == player1:
                    count +=1
            if count ==3:
                return True
        return False
    
    def check_column(board1, player1):
        for i in range(len(board1)):
            count =0
            for j in range(len(board1)):
                if board1[j][i] == player1:
                    count +=1
            if count ==3:
                return True
        return False    

    def check_dialouge(board1,player1):
        count = 0
        for i in range(len(board1)):
            if board1[i][i] == player1:
                count +=1
        if count == 3:
            return True
        return False

    def check_dialouge_reverse(board1,player1):
        count = 0 
        for i in range(len(board1)-1,-1,-1):
            if board1[i][len(board1)-1-i] == player1:
                count +=1
        if count == 3:
            return True
        return False


    if check_row(board,X) or check_column(board,X) or check_dialouge(board,X) or check_dialouge_reverse(board,X):
        return X

    elif check_row(board,O) or check_column(board,O) or check_dialouge(board,O) or check_dialouge_reverse(board,O):
        return O
    else:
        return None

    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    else:
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == EMPTY:
                    return False
        return True 

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # minimax function with max value
    def minimax_max_value(board):
        v = -math.inf
        if terminal(board):
            return utility(board)
        for action in actions(board):
            v = max(v, minimax_min_value(result(board,action)))
        return v

    # minimax function with min value
    def minimax_min_value(board):
        v = math.inf
        if terminal(board):
            return utility(board)
        for action in actions(board):
            v = min(v, minimax_max_value(result(board,action)))
        return v



    if terminal(board):
        return None
    
    elif player(board) == X:
        arr = []
        for action in actions(board):
            arr.append((minimax_min_value(result(board,action)), action))
        move = -math.inf
        for pair in arr:
            if pair[0] > move:
                move = pair[0]
            else:
                move = move

        for pair in arr:
            if pair[0] == move:
                return pair[1]

    elif player(board) == O:
        arr = []
        for action in actions(board):
            arr.append((minimax_max_value(result(board,action)), action))
        move = math.inf
        for pair in arr:
            if pair[0] < move:
                move = pair[0]
            else:
                move = move

        for pair in arr:
            if pair[0] == move:
                return pair[1]

    