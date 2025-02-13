from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import os, secrets, json
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room


from gameLogic import *
from randomAI import *

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)      # make secret key using random
CORS(app)  # To allow React to make cross-origin requests
socketio = SocketIO(app)


rooms = {}  # Dictionary to track game rooms (PvP mode)

# Main menu. User can choose either single player mode or PvP mode
@app.route("/", methods=['GET', 'POST'])
def main():
    print(rooms)
    if request.method == 'GET':
        return render_template('main.html')

    if request.method == 'POST':
        pressed_button = request.form.get('button')  # Get the value of the pressed button

        # Single Player Mode
        if pressed_button == 'single':      # starts single player mode
            session['board'] = initialize_board()      # initialize and store the board in session
            session['curr_player'] = 'B'                          # initialize and store the current player
            return redirect(url_for('single_mode'))  # Redirect to the single mode route

        # PvP mode
        elif pressed_button == 'create':            # Create room for PvP mode
            room_id = random.randint(100000, 999999)          # Generate unique room id
            session['room_id'] = room_id            # Store room ID in session
            session['name'] = "Player1"
            session['hand'] = 'B'
            rooms[room_id] = {
                'players': [],                  # store player name and their hand
                'board': initialize_board(),    # initialize board
                'turn' : 'B'
            }
            rooms[room_id]['players'].append(("Player1", 'B'))
            return redirect(url_for('pvp_room', room_id = room_id))     # Redirect to the room

        elif pressed_button == 'join':
            room_id = int(request.form.get('game_id'))  # Get the entered game ID
            # check if the room exists and there is only one player.
            if room_id in rooms and len(rooms[room_id]['players']) == 1:
                session['room_id'] = room_id
                session['name'] = "player2"
                session['hand'] = 'W'
                rooms[room_id]['players'].append(('Player2', 'W'))
                return redirect(url_for('pvp_room', room_id=room_id))  # Redirect to room
            else:
                return render_template('main.html', error="Invalid Room ID")  # Show an error message

#############################################################################
# This is for single player mode
@app.route("/single-mode/", methods=['GET'])
def single_mode():
    if request.method == 'GET':

        #get the data from session
        board = session.get('board')
        curr_player = session.get('curr_player')

        # make JSON data
        datas = {
            'board' : board,
            'curr_player' : curr_player,
            'valid' : True,
            'message' : 'good',
            'game_over': False
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

    valid_places = get_valid_place(board, curr_player)
    if (row,col) in valid_places:
        board = update_board(board, curr_player, row, col, valid_places[(row, col)])
        curr_player = 'W' if curr_player == 'B' else 'B'

        # Update the session
        session['board'] = board
        session['curr_player'] = curr_player

        endcheck = game_end(board)

        return jsonify({'board': board, 'curr_player': curr_player, 'valid': True, 'message': "good", 'game_over': endcheck})

    else:
        return jsonify({'board': board, 'curr_player': curr_player, 'valid': False, 'message': 'Invalid move.', 'game_over': False})
@app.route("/single-mode/ai/", methods=['POST'])
def ai_turn():
    board = session.get('board')
    curr_player = session.get('curr_player')

    # AI move
    move = randAI(board, curr_player)

    # No valid move for AI
    if move is None:
        curr_player = 'W' if curr_player == 'B' else 'B'
        session['curr_player'] = curr_player
        return jsonify({'board': board, 'curr_player': curr_player, 'valid': False, 'message': "No valid move for AI", 'game_over': game_end(board)})

    row, col, flipped = move
    # update the board and player
    board = update_board(board, curr_player, row, col, flipped)
    curr_player = 'W' if curr_player == 'B' else 'B'

    # Update the session
    session['board'] = board
    session['curr_player'] = curr_player

    # check if player has a valid move.
    valid_places = get_valid_place(board, curr_player)
    # if there is no valid place
    if len(valid_places) == 0:
        curr_player = 'W' if curr_player == 'B' else 'B'
        session['curr_player'] = curr_player
        endcheck = game_end(board)
        return jsonify(
            {'board': board, 'curr_player': curr_player, 'valid': True, 'message': "good", 'game_over': endcheck})

    endcheck = game_end(board)
    print(row, col)
    return jsonify({'board': board, 'curr_player': curr_player, 'valid': True, 'message': "good", 'game_over': endcheck})

@app.route("/single-mode/result/", methods=['POST'])
def game_result():
    board = session.get('board')
    winner, black_score, white_score = result(board)
    if winner == 0:
        player = "tie"
    elif winner == 1:
        player = "Black"
    else:
        player = "White"

    return jsonify({
        'winner': player,
        'black': black_score,
        'white': white_score
    })

#############################################################
# This is for PvP mode
@app.route('/pvp/<int:room_id>', methods=['GET','POST'])
def pvp_room(room_id):
    if request.method == 'GET':
        print(rooms[room_id])
        return render_template('pvp_room.html', room_id=room_id)


@socketio.on('game', namespace='/pvp_room')
def start_game(data):
    room_id = data.get('room_id')
    if len(rooms.get(room_id, {}).get('players', [])) == 2:
        print("Game starts!!")
        emit('game_start', {'message': 'Game has started!'}, room=room_id)


###########################################################
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)