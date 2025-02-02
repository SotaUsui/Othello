# AI that respond randomly for single player mode
import gameLogic
import random

# return row, col, and flipped discs.
def randAI(board, p):

    # get valid places
    places = gameLogic.get_valid_place(board, p)
    if len(places) == 0:
        return None         # there is no place to put

    # choose the place randomly
    key = random.choice(list(places.keys()))
    row, col = key
    flipped = places[key]

    return row, col, flipped