# This is a game logic for othello
# board is represented by r and c. (0,0) is top left. (0,7) is top right.
#   0  1  2  3  4  5  6  7
# 0
# 1
# 2
# 3          W  B
# 4          B  W
# 5
# 6
# 7
# This is an initial board. w is white. b is black.


# Initialize 8x8 board
def initialize_board():
    board = [[' ' for _ in range(8)] for _ in range(8)]         # board represents by list of list
    # put the initialize discs
    board[3][3] = 'W'
    board[3][4] = 'B'
    board[4][3] = 'B'
    board[4][4] = 'W'

    return board

# Update board by the current player's move.
def update_board(board, player, r, c, flipped):
    pass

# Get valid place of the current player
def get_valid_place(board, player):

    # return valid positions and each possible flipped discs' positions
    pass

# Get score of black and white
def get_score(board):
    black = 0
    white = 0
    for r in range(8):
        for c in range(8):
            if board[r][c] == 'B':
                black +=1
            elif board[r][c] == 'W':
                white +=1

    return black, white     # return two scores


def game_end(board):
    pass

# Return win player and score too.
def result(board):
    black, white = get_score(board)

    if black > white:
        winner = 1    # 1 mean black win
    elif white > black:
        winner = 2    # 2 mean white win
    else:
        winner = 0    # 0 mean tie

    return winner, black, white

b = initialize_board()
winner, bl, wh = result(b)
print(winner)
print(bl)

