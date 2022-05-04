from game import Game
from flask import Flask, request

app = Flask(__name__)

game = None

@app.route('/')
def home():
    global game
    game = Game()
    return game.display()

@app.route('/', methods=['POST'])
def guess():
    global game
    if game is None:
        game = Game()
    text = request.form['guess']
    game.guess(text)
    return game.display()
