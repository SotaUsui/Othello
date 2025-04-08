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
    "00": 500, "01": -75, "02": 5, "03":5, "04":5, "05":5, "06":-75, "07":500,
    "10": -75, "11": -75, "12": -1, "13": -1, "14": -1, "15": -1, "16": -75, "17": -75,
    "20": 5, "21": -1, "26": -1, "27": 5,
    "30": 5, "31": -1, "33": 10, "34": 10, "36": -1, "37": 5,
    "40": 5, "41": -1, "43": 10, "44": 10, "46": -1, "47": 5,
    "50": 5, "51": -1, "56": -1, "57": 5,
    "60": -75, "61": -75, "62": -1, "63": -1, "64": -1, "65": -1, "66": -75, "67": -75,
    "70": 500, "71": -75, "72": 5, "73": 5, "74": 5, "75": 5, "76": -75, "77": 500,
}

# check if the player has a disc at corner
def corner_check(board, player):
    score = 0

    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    for row, col in corners:
        if board[row][col] == player:
            pos = f"{row}{col}"
            score += score_map[pos]

    return score

# check if the player has a disc in the middle
def center_check(board, player):
    score = 0

    middle =[(3, 3), (3, 4), (4, 3), (4, 4)]
    for row, col in middle:
        if board[row][col] == player:
            pos = f"{row}{col}"
            score += score_map[pos]

    return score

# evaluate next player move
def eval_next_move(board, player):
    score =0
    valid_positions = gameLogic.get_valid_place(board, player)
    for row, col in valid_positions:
        pos = str(row) + str(col)
        if pos in score_map:
            score += score_map[pos]

    return score


# return difference of disc.
def diff_disc(black, white):
    # It is important in the end of the game.
    return (white-black)*10

##########################################################
def heuristic(board, player):
    score =0
    num_disc, black, white = gameLogic.count_disc(board)


    # Check the corner of the board.
    if player == "W":
        score += corner_check(board, player)
    else:
        score -= corner_check(board, player)

    # evaluate next move
    if player == "W":
        score += eval_next_move(board, player)
    else:
        score -= eval_next_move(board, player)

    # Divide to early stages and late stages.
    # early stage
    if num_disc < 30:
        if player == "W":
            score += center_check(board, player)
        if player == "B":
            score -= center_check(board, player)

    # Late stage
    if num_disc > 53:
        # Difference in number of stones. It is important only for last scene.
        score += diff_disc(black, white)

    return score

#############################################################

# Minimax function to determine the best move for the AI
# Updated to alpha-beta pruning.
def minimax(board, depth, currPlayer, alpha, beta):
    is_terminal = gameLogic.game_end(board)

    # Terminal state evaluation (game over: win/loss/draw)
    # here is where you will add Max depth and the return of the evaluation function
    if is_terminal:
        winner, _, _ = gameLogic.result(board)  # winner(0:tie, 1: black, 2: white)
        if winner == 2:
            return None, None, 10000000000
        elif winner == 1:
            return None, None, -10000000000
        elif winner == 0:  # tie
            return None, None, 0

    if depth == 0:
        return None, None, heuristic(board, currPlayer)    # currPlayer is who will put the disc.

    valid_moves = gameLogic.get_valid_place(board, currPlayer)
    if not valid_moves:
        # return the evaluation of the opponent's board and their possible move
        if currPlayer == "W":
            return minimax(board, depth, "B", alpha, beta)
        else:
            return minimax(board, depth, "W", alpha, beta)

    # Maximize
    if currPlayer == "W":
        value = -math.inf
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

        for _move in valid_moves:
            new_board = copy.deepcopy(board)
            row, col = _move
            new_board = gameLogic.update_board(new_board, "B", row, col, valid_moves[_move])
            new_score = minimax(new_board, depth - 1, "W", alpha, beta,)[2]

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
    place, flipped, score = minimax(board, depth, currPlayer, alpha, beta)     # place is turple, flipped is list
    if place is None:
        return None, None, None
    row, col = place
    return row, col, flipped