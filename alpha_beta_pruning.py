# AI that respond using alpha-beta pruning for single player mode
# get board and current player and return move which is (row, col, flipped_disc). flipped_disc is list
import math
import copy
import random
import gameLogic



# [200,-50, 5, 5, 5, 5,-50,200]
# [-50,-50,-1,-1,-1,-1,-50,-50]
# [5  , -1, 0, 0, 0, 0, -1,  5]
# [5  , -1, 0, 1, 1, 0, -1,  5]
# [5  , -1, 0, 1, 1, 0, -1,  5]
# [5  , -1, 0, 0, 0, 0, -1,  5]
# [-50,-50,-1,-1,-1,-1,-50,-50]
# [200,-50, 5, 5, 5, 5,-50,200]
score_map = {
    "11": 200, "12": -50, "13": 5, "14":5, "15":5, "16":5, "17":-50, "18":200,
    "21": -50, "22": -50, "23": -1, "24": -1, "25": -1, "26": -1, "27": -50, "28": -50,
    "31": 5, "32": -1, "37": -1, "38": 5,
    "41": 5, "42": -1, "44": 1, "45": 1, "47": -1, "48": 5,
    "51": 5, "52": -1, "54": 1, "55": 1, "57": -1, "58": 5,
    "61": 5, "62": -1, "67": -1, "68": 5,
    "71": -50, "72": -50, "73": -1, "74": -1, "75": -1, "76": -1, "77": -50, "78": -50,
    "81": 200, "82": -50, "83": 5, "84": 5, "85": 5, "86": 5, "87": -50, "88": 200,
}

# assign value for position
def value_position(move, player):
    score =0
    row, col = move
    pos = str(row) + str(col)
    if pos in score_map:
        score += score_map[pos]

    if player == "B":
        return -score

    return score

# return difference of disc.
def diff_disc(black, white):
    # It is important in the end of the game.
    return (white-black)*10


# return the mobility for the next player
def mobility(board, player):
    next_player = "B" if player == "W" else "W"
    valid_moves = gameLogic.get_valid_place(board, next_player)
    score = 0

    if not valid_moves:
        return score

    for move in valid_moves:
        row, col = move
        pos = str(row) + str(col)
        if pos in score_map:
            score += score_map[pos]

    if next_player == "B":
        return -1*score

    return score



def heuristic(board, player, move):
    score =0
    num_disc, black, white = gameLogic.count_disc(board)

    # Value of move
    if move is not None:
        score += value_position(move, player)  # player should be "W", since AI is always white turn

    # Divide to early stages, midway, and late stages.
    # Late stage
    if num_disc > 53:
        # Difference in number of stones. It is important only for last scene.
        score += diff_disc(black, white)

    # Early stages, and midway.
    else:
        # Difference of mobility (number of legal hands). It's import for beginning of the game.
        score += mobility(board, player)

    return score


# Minimax function to determine the best move for the AI
# Updated to alpha-beta pruning.
def minimax(board, depth, currPlayer, alpha, beta, last_move):
    valid_moves = gameLogic.get_valid_place(board, currPlayer)      # {place: [flipped]}
    is_terminal = gameLogic.game_end(board)

    # Terminal state evaluation (game over: win/loss/draw)
    # here is where you will add Max depth and the return of the evaluation function
    if is_terminal:
        winner, _, _ = gameLogic.result(board)  # winner(0:tie, 1: black, 2: white)
        if winner == 2:
            return last_move, None, 10000000000
        elif winner == 1:
            return last_move, None, -10000000000
        elif winner == 0:  # tie
            return last_move, None, 0

    if depth == 0:
        return last_move, None, heuristic(board, currPlayer, last_move)

    if not valid_moves:
        # return the evaluation of the opponent's board and their possible move
        if currPlayer == "W":
            return minimax(board, depth, "B", alpha, beta, last_move)
        else:
            return minimax(board, depth, "W", alpha, beta, last_move)

    # Maximize
    if currPlayer == "W":
        value = -math.inf
        move = None
        for _move in valid_moves:
            new_board = copy.deepcopy(board)
            row,col = _move
            new_board = gameLogic.update_board(new_board, "W", row, col, valid_moves[_move])
            new_score = minimax(new_board, depth - 1, "B", alpha, beta, _move)[2]

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
            new_score = minimax(new_board, depth - 1, "W", alpha, beta, _move)[2]

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
    depth = 5           # searching depth
    best_move = None
    alpha = -math.inf   # best (highest) value the maximizing player can guarantee. (best score for yourself)
    beta = math.inf     # best (lowest) value the minimizing player can guarantee.  (worst score for opponent)
    # AI is always white
    last_move = None        # should be turple of (col, row)
    place, flipped, score = minimax(board, depth, currPlayer, alpha, beta, last_move)     # place is turple, flipped is list
    if place is None:
        return None, None, None
    row, col = place
    print(score)
    return row, col, flipped