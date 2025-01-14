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
    board = [['-' for _ in range(8)] for _ in range(8)]         # board represents by list of list
    # put the initialize discs
    board[3][3] = 'W'
    board[3][4] = 'B'
    board[4][3] = 'B'
    board[4][4] = 'W'

    return board

# Update board by the current player's move.
def update_board(board, player, row, col, flipped):
    board [row][col] = player           # put the disc
    for r, c in flipped:
        board[r][c] = player        # flip the discs

    return board

# Get valid place of the current player
# Return valid positions and each expected flipped discs' positions
def get_valid_place(board, player):
    opponent = 'W' if player == 'B' else 'B'        # define opponent's disc color
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    valid_positions = {}        # this is the set of position and expected flipped discs

    for row in range(8):
        for col in range(8):
            # only check when the spot is not occupied
            if board[row][col] == '-':
                flipped_positions = []

                # check all the directions
                for dr, dc in directions:
                    r,c = row + dr, col + dc
                    temp_flipped = []

                    # proceed as long as the opponent's piece lasts.
                    while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
                        temp_flipped.append((r, c))
                        # move to next spot
                        r += dr
                        c += dc

                    # valid only if the player can pinch it with own piece.
                    if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                        flipped_positions.extend(temp_flipped)

                # store if there is a spot that player can put
                if flipped_positions:
                    valid_positions[(row, col)] = flipped_positions

    return valid_positions

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

# Either board is full or both of the player can't put the disc.
def game_end(board):
    pass

# Return win player and score too.
def result(board):
    black, white = get_score(board)
    winner = 0          # 0 mean tie
    if black > white:
        winner = 1    # 1 mean black win
    elif white > black:
        winner = 2    # 2 mean white win

    return winner, black, white

board = initialize_board()
print(board)
while (True):
    sets = get_valid_place(board, 'B')
    print(sets)
    r,c = map(int, input().split())
    board = update_board(board, 'B', r, c, sets[r,c])
    print(board)

    sets = get_valid_place(board, 'W')
    print(sets)
    r, c = map(int, input().split())
    board = update_board(board, 'W', r, c, sets[r,c])
    print(board)





