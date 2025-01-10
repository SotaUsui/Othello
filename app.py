from flask import Flask, request, render_template, redirect, url_for, session
import os, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)      # make secrt key using random


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('main.html')

    if request.method == 'POST':
        pressed_button = request.form.get('button')  # Get the value of the pressed button

        if pressed_button == 'single':      # starts single player mode
            return "single player mode"
        elif pressed_button == 'pvp':       # starts PvP mode
            return "pvp mode"
