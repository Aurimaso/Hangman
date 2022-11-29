from flask_app import db
from sqlalchemy import DateTime
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String(50))
    email = db.Column("Email", db.String(180), unique=True, nullable=False)
    password = db.Column("Password", db.String(100), nullable=False)
    games = db.relationship('Game', backref='users')

class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    outcome = db.Column("Outcome", db.String(10))
    word = db.Column("Word", db.String(30))
    guesses_made = db.Column("Guesses", db.String(20))
    progress = db.Column("Progress", db.String(30))
    mistakes = db.Column("Mistakes", db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, outcome, word, guesses_made, progress, mistakes, user_id) -> None:
        self.outcome = outcome
        self.guesses_made = guesses_made
        self.user_id = user_id
        self.word = word
        self.progress = progress
        self.mistakes = mistakes