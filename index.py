from dataclasses import dataclass
from flask import Flask, jsonify,  request, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from typing import List

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'my_secret_key'

db = SQLAlchemy(app)

@dataclass
class Player(db.Model):
    id: int
    username: str
    password: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    

    def __repr__(self):
        return f'<Player {self.username}>'
    
    def check_password(self, password):
        return self.password == password

@dataclass
class Game(db.Model):
    id: int
    player1_id: int
    player2_id: int
    board: List[int]

    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, nullable=False)
    player2_id = db.Column(db.Integer, nullable=False)
    board = db.Column(db.PickleType, nullable=False, default=[0, 0, 0, 0, 0, 0, 0, 0, 0])

    def __repr__(self):
        return f'<Game {self.id}>'

with app.app_context():
    db.create_all()

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/signup_menu')
def signup_menu():
    return render_template('signup.html')

@app.route('/game_menu')
def game_menu():
    return render_template('game.html')

@app.route('/login_menu')
def login_menu():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    player = Player.query.filter_by(username=data["username"]).first()
    if player and player.check_password(data["password"]):
        return 'SUCCESS'
    else:
        flash('Invalid username or password')
        return redirect('/login_menu')
    
@app.route('/games', methods=['POST', 'GET', 'DELETE'])
def route_games():
    if request.method == 'POST':
        data = request.get_json()
        game = Game(player1_id=data["player1_id"], player2_id=data["player2_id"])
        db.session.add(game)
        db.session.commit()
        return "SUCCESS"
    elif request.method == 'GET':
        games = Game.query.all()
        return jsonify(games)
    elif request.method == 'DELETE':
        games = Game.query.all()
        for game in games:
            db.session.delete(game)
        db.session.commit()
        return "SUCCESS"

@app.route('/games/<game_id>', methods=['GET', 'DELETE', 'PUT'])
def route_games_id(game_id):
    if request.method == 'GET':
        game = Game.query.get_or_404(game_id)
        return jsonify(game)
    elif request.method == 'DELETE':
        game = Game.query.get_or_404(game_id)
        db.session.delete(game)
        db.session.commit()
        return "SUCCESS"
    elif request.method == 'PUT':
        data = request.get_json()
        game = Game.query.get_or_404(game_id)
        game.board = data["board"]
        db.session.commit()
        return "SUCCESS"

@app.route('/players', methods=['GET', 'POST'])
def route_players():
    if request.method == 'GET':
        return get_players()
    elif request.method == 'POST':
        player = request.get_json()
        return insert_player(player)

@app.route('/players/<player_id>', methods=['GET', 'PUT', 'DELETE'])
def route_players_id(player_id):
    if request.method == 'GET':
        return get_player_by_id(player_id)
    elif request.method == 'PUT':
        player = request.get_json()
        return update_player(player_id, player)
    elif request.method == 'DELETE':
        return delete_player(player_id)

def get_players():
    players = Player.query.all()
    return jsonify(players)

def get_player_by_id(player_id):
    player = Player.query.get_or_404(player_id)
    return jsonify(player)

def insert_player(data):
    player = Player(username=data["username"], password=data["password"])
    db.session.add(player)
    db.session.commit()
    return "SUCCESS"

def update_player(player_id, new_player):
    player = Player.query.get_or_404(player_id)
    player.username = new_player["username"]
    player.password = new_player["password"]
    db.session.commit()
    return 'SUCCESS'

def delete_player(player_id):
    player = Player.query.get_or_404(player_id)
    db.session.delete(player)
    db.session.commit()
    return "SUCCESS"