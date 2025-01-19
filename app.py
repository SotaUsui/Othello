from flask import Flask, request, render_template, redirect, url_for, session
import os, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)      # make secret key using random

# Main menu. User can choose either single player mode or PvP mode
@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('main.html')

    if request.method == 'POST':
        pressed_button = request.form.get('button')  # Get the value of the pressed button

        if pressed_button == 'single':      # starts single player mode
            return redirect(url_for('single'))  # Redirect to the single mode route
        elif pressed_button == 'pvp':       # starts PvP mode
            return redirect(url_for('pvp'))     # Redirect to the PvP mode route

#############################################################################
# This is for single player mode
@app.route("single-mode", methods=['GET', 'POST'])
def single_mode():
    # draw the board
    if request.method == 'GET':
        return render_template('single.html')

    # Get move from user
    if request.method == 'POST':
        # check if the move is valid

        # update the move

        # draw the board

        # check if the game end. If it is, jump to result page.

        # move by AI

        # check if the game end. If it is, jump to result page.

        # draw the board


########################################################################
# This is for PvP mode