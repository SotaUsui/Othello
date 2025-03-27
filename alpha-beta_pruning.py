# AI that respond using alpha-beta pruning for single player mode
# get board and current player and return move which is (row, col, flipped_disc). flipped_disc is list
import math
import gameLogic







def smartAI(board, currPlayer):
    depth = 4           # searching depth
    best_move = None
    alpha = -math.inf   # best (highest) value the maximizing player can guarantee. (best score for yourself)
    beta = math.inf     # best (lowest) value the minimizing player can guarantee.  (worst score for opponent)

