from flask import Flask, request, render_template, redirect, url_for, session
import os, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)      # make secrt key using random


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('main.html')

    #if request.method == 'POST':
