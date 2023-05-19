from dataclasses import dataclass
from flask import Flask, jsonify, request, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

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
    logged: bool
    in_game: bool

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    logged = db.Column(db.Boolean, nullable=False, default=False)
    in_game = db.Column(db.Boolean, nullable=False, default=False)
    
    def __repr__(self):
        return f'<Player {self.username}>'
    
    def check_password(self, password):
        return self.password == password

@dataclass
class Game(db.Model):
    id: int
    player1_id: int
    player2_id: int
    board: str

    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, nullable=False)
    player2_id = db.Column(db.Integer, nullable=False)
    board = db.Column(db.String, nullable=False, default="_________")

    def __repr__(self):
        return f'<Game {self.id}>'

with app.app_context():
    db.create_all()

@app.route('/list')
def list():
    return render_template('list.html')

@app.route('/list.js')
def list_js():
    return render_template('list.js')

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/login.js')
def login_js():
    return render_template('login.js')

@app.route('/signup_menu')
def signup_menu():
    return render_template('signup.html')

@app.route('/game_menu')
def game_menu():
    try:
        username = request.args.get('username')
        current_player = Player.query.filter_by(username=username).first()
        available_games = Game.query.all()
        return render_template('game_menu.html', logged_in=current_player.logged, in_game=current_player.in_game, current_player=current_player, available_games=available_games)
    except:
        return "NO USERNAME PROVIDED"


@app.route('/login_menu')
def login_menu():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    player = Player.query.filter_by(username=data["username"]).first()
    if player and player.check_password(data["password"]):
        player.logged = True
        db.session.commit()
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
        index = data["index"]

        game = Game.query.get_or_404(game_id)
        new_string = game.board[:index] + 'X' + game.board[index + 1:]
        game.board = new_string

        db.session.add(game)
        db.session.commit()
        return "SUCCESS"

@app.route('/players', methods=['GET', 'POST'])
def route_players():
    if request.method == 'GET':
        players = Player.query.all()
        return jsonify(players)
    
    elif request.method == 'POST':
        data = request.get_json()
        player = Player(username=data["username"], password=data["password"])
        
        try:
            db.session.add(player)
            db.session.commit()
            return "SUCCESS"
        except IntegrityError:
            db.session.rollback()
            return "Player with the same username already exists."

@app.route('/players/<player_id>', methods=['GET', 'PUT', 'DELETE'])
def route_players_id(player_id):
    if request.method == 'GET':
        player = Player.query.get_or_404(player_id)
        return jsonify(player)
    
    elif request.method == 'PUT':
        data = request.get_json()
        player = Player.query.get_or_404(player_id)
        player.username = data["username"]
        player.password = data["password"]
        db.session.commit()
        return 'SUCCESS'
    
    elif request.method == 'DELETE':
        player = Player.query.get_or_404(player_id)
        db.session.delete(player)
        db.session.commit()
        return "SUCCESS"
    

