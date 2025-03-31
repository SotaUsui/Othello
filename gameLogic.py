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

# Count disc on the board
def count_disc(board):
    white = 0
    black = 0
    for line in board:
        white += line.count('W')
        black += line.count("B")

    return white+black, black, white


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
    # check if the board is full
    full = True
    for row in board:
        if '-' in row:
            full = False
            break           # There is still an empty spot
    if full:
        return True         # board is full

    # check the player's valid move
    b_move = get_valid_place(board, 'B')
    w_move = get_valid_place(board, 'W')

    if not b_move and not w_move:
        return True         # neither player can put disc.

    return False

# Return win player and score too.
def result(board):
    black, white = get_score(board)
    winner = 0          # 0 mean tie
    if black > white:
        winner = 1    # 1 mean black win
    elif white > black:
        winner = 2    # 2 mean white win

    return winner, black, white

'''
###########################
####### play game #########
###########################
board = initialize_board()  # Initialize the board
print("Initial Board:")
for row in board:
    print(" ".join(row))  # Display the board in a readable format

# Keep looping until the game ends
while not game_end(board):
    # Black's turn
    sets = get_valid_place(board, 'B')
    if sets:  # If Black has valid moves
        print("Black's Turn")
        print("Valid Moves:", sets)
        r, c = map(int, input("Enter row and column (e.g., 3 2): ").split())
        if (r, c) in sets:  # Check if the entered move is valid
            board = update_board(board, 'B', r, c, sets[(r, c)])
        else:
            print("Invalid move. Please try again.")
            continue  # Ask for input again
        print("Board after Black's move:")
        for row in board:
            print(" ".join(row))
    else:
        print("Black has no valid moves. Skipping Black's turn.")

    # Check if the game ends after Black's move
    if game_end(board):
        break

    # White's turn
    sets = get_valid_place(board, 'W')
    if sets:  # If White has valid moves
        print("White's Turn")
        print("Valid Moves:", sets)
        r, c = map(int, input("Enter row and column (e.g., 3 2): ").split())
        if (r, c) in sets:  # Check if the entered move is valid
            board = update_board(board, 'W', r, c, sets[(r, c)])
        else:
            print("Invalid move. Please try again.")
            continue  # Ask for input again
        print("Board after White's move:")
        for row in board:
            print(" ".join(row))
    else:
        print("White has no valid moves. Skipping White's turn.")

# After the game ends, display the results
print("Game End!")
winner, black, white = result(board)
print(f"Final Score -> Black: {black}, White: {white}")
if winner == 1:
    print("Winner: Black")
elif winner == 2:
    print("Winner: White")
else:
    print("It's a tie!")
'''