# AI that respond using alpha-beta pruning for single player mode
# get board and current player and return move which is (row, col, flipped_disc). flipped_disc is list
import math
import copy
import random
import gameLogic


# assign value for position
def value_position(board, player):
    # [200,-50, 5, 5, 5, 5,-50,200]
    # [-50,-50,-1,-1,-1,-1,-50,-50]
    # [5  , -1, -, -, -, -, -1,  5]
    # [5  , -1, -, 1, 1, -, -1,  5]
    # [5  , -1, -, 1, 1, -, -1,  5]
    # [5  , -1, -, -, -, -, -1,  5]
    # [-50,-50,-1,-1,-1,-1,-50,-50]
    # [200,-50, 5, 5, 5, 5,-50,200]
    score_map = {
        "11": 1000, "12": -500, "13": 15, "14":15, "15":15, "16":15, "17":-500, "18":1000,
        "21": -500, "22": -500, "23": -10, "24": -10, "25": -10, "26": -10, "27": -500, "28": -500,
        "31": 15, "32": -10, "37": -10, "38": 5,
        "41": 15, "42": -10, "44": 50, "45": 50, "47": -10, "48": 15,
        "51": 15, "52": -10, "54": 50, "55": 50, "57": -10, "58": 15,
        "61": 15, "62": -10, "67": -10, "68": 15,
        "71": -500, "72": -500, "73": -10, "74": -10, "75": -10, "76": -10, "77": -500, "78": -500,
        "81": 1000, "82": -500, "83": 15, "84": 15, "85": 15, "86": 15, "87": -500, "88": 1000,
    }

    score =0
    for i in range(8):
        row = i+1
        for j in range(8):
            col = j+1
            if board[i][j] == player:
                place = str(row) + str(col)
                if place in score_map:
                    score += score_map[place]

    return score

# return difference of disc.
def diff_disc(black, white):
    # It is important in the end of the game.
    return (white-black)*10


def diff_mobi(board, player):
    # AI is always white
    AI_mobi = len(gameLogic.get_valid_place(board, player))

    return (w_mobi - b_mobi)*2


def heuristic(board, player):
    score =0
    num_disc, black, white = gameLogic.count_disc(board)

    # Value of board position
    score += value_position(board, player)  # player should be "W", since AI is always white turn

    # Divide to early stages, midway, and late stages.
    # Late stage
    if num_disc > 53:
        # Difference in number of stones. It is important only for last scene.
        score += diff_disc(black, white)
    # Early stages, and midway.
    #else:
        # Difference of mobility (number of legal hands). It's import for beginning of the game.
        #score += diff_mobi(board, player)


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

    if not valid_moves:
        # return the evaluation of the opponent's board and their possible moves
        return None, None, heuristic(board, currPlayer)

    # Maximize
    if currPlayer == "W":
        value = -math.inf
        move = None
        for _move in valid_moves:
            new_board = copy.deepcopy(board)
            row,col = _move
            new_board = gameLogic.update_board(new_board, "W", row, col, valid_moves[_move])
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
            new_board = gameLogic.update_board(new_board, "B", row, col, valid_moves[_move])
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
    depth = 4           # searching depth
    best_move = None
    alpha = -math.inf   # best (highest) value the maximizing player can guarantee. (best score for yourself)
    beta = math.inf     # best (lowest) value the minimizing player can guarantee.  (worst score for opponent)
    # AI is always white
    place, flipped, score = minimax(board, depth, currPlayer, alpha, beta)     # place is turple, flipped is list
    row, col = place
    return row, col, flipped