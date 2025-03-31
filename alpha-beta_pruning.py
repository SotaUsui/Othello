# AI that respond using alpha-beta pruning for single player mode
# get board and current player and return move which is (row, col, flipped_disc). flipped_disc is list
import math
import copy
import random
import gameLogic


# assign value for position
def value_position(board):
    # [200,-25, 5, 5, 5, 5,-25,200]
    # [-25,-25,-1,-1,-1,-1,-25,-25]
    # [5  , -1, -, -, -, -, -1,  5]
    # [5  , -1, -, 1, 1, -, -1,  5]
    # [5  , -1, -, 1, 1, -, -1,  5]
    # [5  , -1, -, -, -, -, -1,  5]
    # [-25,-25,-1,-1,-1,-1,-25,-25]
    # [200,-25, 5, 5, 5, 5,-25,200]

    score =0


    return score


def heuristic(board, player):
    score =0

    # Value of board position
    score += value_position(board)

    # Difference in number of stones

    # Difference of mobility (number of legal hands)

    return score


# Minimax function to determine the best move for the AI
# Updated to alpha-beta pruning.
def minimax(board, depth, currPlayer, alpha, beta):
    valid_moves = gameLogic.get_valid_place(board, currPlayer)      # {place: [flipped]}
    is_terminal = gameLogic.game_end(board)

    # Terminal state evaluation (game over: win/loss/draw)
    # here is where you will add Max depth and the return of the evaluation function
    if depth == 0 or is_terminal:
        winner, _, _ = gameLogic.result(board)      # winner(0:tie, 1: black, 2: white)
        if winner == 1:
            return (None, None, 10000000000)
        elif winner == 2:
            return (None, None, -10000000000)
        elif winner == 0:   # tie
            return(None, None, 0)
        else:   # Game over, no moves left
            return (None, None, heuristic(board, "W"))      # AI is White

    # Maximize
    if currPlayer == "W":
        value = -math.inf
        move = None
        for _move in valid_moves:
            new_board = copy.deepcopy(board)
            row,col = _move
            new_board = gameLogic.update_board(board, "W", row, col, valid_moves[_move])
            new_score = minimax(new_board, depth - 1, "B", alpha, beta)[2]

            # update value and alpha
            if new_score > value:
                value = new_score
                move = _move
            alpha = max(alpha, value)

            # alpha-beta pruning
            if alpha >= beta:
                break      # cut off. It makes program more efficient.

        return move, valid_moves[move], value

    # Minimize
    else:
        value = math.inf
        move = None

        for _move in valid_moves:
            new_board = copy.deepcopy(board)
            row, col = _move
            new_board = gameLogic.update_board(board, "B", row, col, valid_moves[_move])
            new_score = minimax(new_board, depth - 1, "W", alpha, beta)[2]

            # update value and beta
            if new_score < value:
                value = new_score
                move = _move
            beta = min(beta, value)

            # alpha-beta pruning
            if alpha >= beta:
                break

        return move, valid_moves[move], value



def smartAI(board, currPlayer):
    depth = 3           # searching depth
    best_move = None
    alpha = -math.inf   # best (highest) value the maximizing player can guarantee. (best score for yourself)
    beta = math.inf     # best (lowest) value the minimizing player can guarantee.  (worst score for opponent)
    # AI is always white
    place, flipped, score = minimax(board, depth, currPlayer, alpha, beta)     # place is turple, flipped is list
    row, col = place
    return row, col, flipped