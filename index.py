from dataclasses import dataclass
from flask import Flask, jsonify,  request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@dataclass
class Player(db.Model):
    id: int
    firstname: str
    lastname: str

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    

    def __repr__(self):
        return f'<Player {self.firstname}>'
    
def test_connection():
    with app.app_context():
        db.create_all()
        player_test = Player(firstname='john', lastname='doe')

        db.session.add(player_test)
        db.session.commit()

        students = Player.query.all()

        print(students)
        print(jsonify(students))

test_connection()

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/players', methods=['GET'])
def route_get_players():
    return get_players()

@app.route('/players/<player_id>', methods=['GET'])
def route_get_player(player_id):
    return get_player_by_id(player_id)

@app.route('/players/add',  methods = ['POST'])
def route_add_player():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    player = Player(firstname=firstname, lastname=lastname)
    db.session.add(player)
    db.session.commit()
    return redirect('/')

@app.route('/players/delete', methods=['POST', 'DELETE'])
def route_delete_player():
    player_id = request.form['player_id']
    player = Player.query.get(player_id)
    if player is None:
        error_message = f"No player with ID {player_id} found."
        return render_template('menu.html', error_message=error_message)
    db.session.delete(player)
    db.session.commit()
    return redirect('/')

@app.route('/players/delete/<player_id>', methods=['GET','DELETE'])
def route_delete_player2(player_id):
    return delete_player(player_id)

@app.route('/players/list', methods=['GET'])
def route_list_players():
    players = Player.query.all()
    return render_template('menu.html', players=players)

def get_players():
    players = Player.query.all()
    return jsonify(players)

def get_player_by_id(player_id):
    player = Player.query.get(player_id)
    return jsonify(player)

def insert_player(firstname, lastname):
    new_player = Player(name=firstname, age=lastname)
    db.session.add(new_player)
    db.session.commit()
    return new_player.id

def delete_player(player_id):
    player = Player.query.get(player_id)
    if player is None:
        return f"No player with ID {player_id} found."
    db.session.delete(player)
    db.session.commit()
    return f"Player with ID {player_id} has been deleted."

# @app.route('/players/update',  methods = ['PUT'])
# def route_update_player():
#     player = request.get_json()
#     return update_player(player)

# def update_player(player_id, name=None, age=None):
#     player = Player.query.get(player_id)
#     if player is not None:
#         if name is not None:
#             player.name = name
#         if age is not None:
#             player.age = age
#         db.session.commit()
#     return