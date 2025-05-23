# http://0.0.0.3000 - local
# http://[ip-address]:3000

"""
from imp import new_module
from gevent import monkey
monkey.patch_all()      # to use gevent
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import os, secrets, json
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
"""
import types
from gevent import monkey
monkey.patch_all()  # to use gevent

from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import os
import secrets
import json
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room

from gameLogic import *
from randomAI import *
from alpha_beta_pruning import *


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)      # make secret key using random
CORS(app)  # To allow React to make cross-origin requests
socketio = SocketIO(app, cors_allowed_origins="*")

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
                'turn' : 'B',                   # assign the hand
                'ready' : {'Player1': False, 'Player2': False}  # ready for the game
            }
            rooms[room_id]['players'].append(("Player1", 'B'))
            return redirect(url_for('pvp_room', room_id = room_id))     # Redirect to the room

        elif pressed_button == 'join':
            room_id = int(request.form.get('game_id'))  # Get the entered game ID
            # check if the room exists and there is only one player.
            if room_id in rooms and len(rooms[room_id]['players']) == 1:
                session['room_id'] = room_id
                session['name'] = "Player2"
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

        _, black, white = count_disc(board)
        # make JSON data
        datas = {
            'board' : board,
            'curr_player' : curr_player,
            'valid' : True,
            'message' : 'good',
            'game_over': False,
            'black': black,
            'white': white
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
        _, black, white = count_disc(board)
        return jsonify({'board': board, 'curr_player': curr_player, 'valid': True, 'message': "good", 'black':black, 'white': white, 'game_over': endcheck})

    else:
        _, black, white = count_disc(board)
        return jsonify({'board': board, 'curr_player': curr_player, 'valid': False, 'message': 'Invalid move.', 'black':black, 'white': white, 'game_over': False})
@app.route("/single-mode/ai/", methods=['POST'])
def ai_turn():
    board = session.get('board')
    curr_player = session.get('curr_player')

    # No valid move for AI
    #if move is None:
    if get_valid_place(board, curr_player) == {}:
        curr_player = 'W' if curr_player == 'B' else 'B'
        session['curr_player'] = curr_player
        _, black, white = count_disc(board)
        return jsonify({'board': board, 'curr_player': curr_player, 'valid': False, 'message': "No valid move for AI", 'black':black, 'white': white ,'game_over': game_end(board)})

    # AI move
    #move = randAI(board, curr_player)
    move = smartAI(board, curr_player)
    row, col, flipped = move
    # update the board and player
    board = update_board(board, curr_player, row, col, flipped)
    curr_player = 'W' if curr_player == 'B' else 'B'

    # Update the session
    session['board'] = board
    session['curr_player'] = curr_player
    _, black, white = count_disc(board)

    # check if player has a valid move.
    valid_places = get_valid_place(board, curr_player)
    # if there is no valid place
    if len(valid_places) == 0:
        curr_player = 'W' if curr_player == 'B' else 'B'
        session['curr_player'] = curr_player
        endcheck = game_end(board)
        return jsonify(
            {'board': board, 'curr_player': curr_player, 'valid': True, 'message': "good", 'black': black, 'white': white,'game_over': endcheck})

    endcheck = game_end(board)
    print(row, col)
    return jsonify({'board': board, 'curr_player': curr_player, 'valid': True, 'message': "good", 'black': black, 'white': white ,'game_over': endcheck})

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
@app.route('/pvp/<int:room_id>')
def pvp_room(room_id):
    print(rooms[room_id])
    player = session.get('name')  # "Player1" or "Player2"
    return render_template('pvp_room.html', room_id=room_id, player=player)

@socketio.on('ready')
def handle_ready(data):
    room_id = int(data['room_id'])
    player = data['player']
    print(f'{player} clicked ready in {room_id}.')

    if room_id in rooms:
        rooms[room_id]['ready'][player] = True
        print(rooms[room_id])
        # Check if both players are ready
        if rooms[room_id]['ready']['Player1'] == True and rooms[room_id]['ready']['Player2'] == True:
            socketio.emit('game_start', {
                "room":room_id
                #"player1": "Player1",
                #"player2": "Player2"
            })

        else:
            print("waiting")
            msg = "Waiting for the opponent..."
            socketio.emit('waiting', {"room":room_id, "message": msg})


@app.route('/game/<int:room_id>/<player>')
def game_page(room_id, player):
    # if room doesn't exist
    if room_id not in rooms:
        return redirect(url_for('main'))  # Redirect to main page

    return render_template('pvp_game.html', room_id=room_id, player=player)

@socketio.on('game_state')
def gema_update(data):
    room_id = data["room_id"]
    # make sure the room id exist
    if room_id in rooms:
        board = rooms[room_id]["board"]
        currPlayer = rooms[room_id]["turn"]
        b,w = get_score(board)
        score = (b,w)
        is_done = game_end(board)
        socketio.emit("game_update", {"board":board, "currPlayer":currPlayer, "score":score, "is_done":is_done})

@socketio.on('player_move')
def pvp_move(data):
    room_id = data["room_id"]
    row, col = data["place"]
    player = data["turn"]   # "B" or "W"

    board = rooms[room_id]["board"]

    # check if player has a valid move.
    valid_places = get_valid_place(board, player)

    if (row,col) in valid_places:
        new_board = update_board(board, player, row, col, valid_places[(row, col)])
        next_player = 'W' if player == 'B' else 'B'

        # Update the room status
        rooms[room_id]["board"] = new_board
        rooms[room_id]["turn"] = next_player

        is_done = game_end(new_board)

        # check if other player has valid move
        valid_places = get_valid_place(new_board, next_player)
        if len(valid_places) == 0:
            next_player = 'W' if next_player == 'B' else 'B'

        b,w = get_score(new_board)
        score = (b,w)
        socketio.emit("game_update", {"board": new_board, "currPlayer": next_player, "score": score, "is_done": is_done})



###########################################################
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000, debug=True, allow_unsafe_werkzeug=True)