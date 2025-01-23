from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import os, secrets, json
from flask_cors import CORS

from gameLogic import *
from randomAI import *

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)      # make secret key using random
CORS(app)  # To allow React to make cross-origin requests


# Main menu. User can choose either single player mode or PvP mode
@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('main.html')

    if request.method == 'POST':
        pressed_button = request.form.get('button')  # Get the value of the pressed button

        if pressed_button == 'single':      # starts single player mode
            session['board'] = initialize_board()      # initialize and store the board in session
            session['curr_player'] = 'B'                          # initialize and store the current player
            return redirect(url_for('single_mode'))  # Redirect to the single mode route
        elif pressed_button == 'pvp':       # starts PvP mode
            return redirect(url_for('pvp'))     # Redirect to the PvP mode route

#############################################################################
# This is for single player mode
@app.route("/single-mode/", methods=['GET'])
def single_mode():
    if request.method == 'GET':
        # Initialize the game and render the front-end
        board = initialize_board()  # Initialize the board
        curr_player = 'B'           # Start with Black

        # make JSON data
        datas = {
            'board' : board,
            'curr_player' : curr_player,
            'valid' : True,
            'message' : 'good'
        }
        return render_template('single.html', data=datas)

# Handle the move by the player
@app.route("/single-mode/move/", methods=['POST'])
def move():
    board = session.get('board')
    curr_player = session.get('curr_player')

    # get the clicked cell from the request
    data = request.json
    row, col = data["row"], data["col"]

    # check if it is valid
    valid_places = get_valid_place(board, curr_player)
    if (row,col) in valid_places:
        board = update_board(board, curr_player, row, col, valid_places[(row, col)])
        curr_player = 'W' if curr_player == 'B' else 'B'

        # Update the session
        session['board'] = board
        session['curr_player'] = curr_player

        return jsonify({'board': board, 'curr_player': curr_player, 'valid': True})

    else:
        return jsonify({'board': board, 'curr_player': curr_player, 'valid': False, 'message': 'Invalid'})
@app.route("/single-mode/ai/", methods=['GET','POST'])
def ai_turn():
    board = session.get('board')
    curr_player = session.get('curr_player')

    # AI move
    row, col, flipped = randAI(board, curr_player)

    # update the board
    board = update_board(board, curr_player, row, col, flipped)
    curr_player = 'W' if curr_player == 'B' else 'B'

    # Update the session
    session['board'] = board
    session['curr_player'] = curr_player

    return jsonify({'board': board, 'current_player': curr_player, 'valid': True})

# check if the game end


#############################################################