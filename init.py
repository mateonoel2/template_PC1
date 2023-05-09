from dataclasses import dataclass
from flask import Flask, jsonify,  request
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
        return f'<player {self.firstname}>'
    

    

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

