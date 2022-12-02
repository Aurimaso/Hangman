# import os
# from flask import Flask, render_template, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

# basedir = os.path.abspath(os.path.dirname(__file__))
# print(basedir)

# app = Flask(__name__)

# app.config['SECRET_KEY'] = 'dfgsfdgsdfgsdfgsdf'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'vaikaitevai.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# app.app_context().push()

# class User(db.Model):
#     __tablename__ = "user"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column("Name", db.String(50))
#     surname = db.Column("Surname", db.String(50))
#     games = db.relationship('Games', backref='user')

#     def __init__(self, name, surname) -> None:
#         self.name = name
#         self.surname = surname

# class Games(db.Model):
#     __tablename__ = "games"
#     id = db.Column(db.Integer, primary_key=True)
#     outcome = db.Column("Outcome", db.String(10))
#     guesses_made = db.Column("guesses", db.String(20))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __init__(self, outcome, guesses_made, user_id) -> None:
#         self.outcome = outcome
#         self.guesses_made = guesses_made
#         self.user_id = user_id

# db.create_all()


# t1 = User('Tevas', 'Tevukas')
# t2 = User('Tomas', 'Tomukas')

# v1 = Games('Won', 'Patevis', 1)
# v2 = Games('Lost', 'Opapa', 2)
# v3 = Games('Lost1', 'Opapa1', 1)

# db.session.add_all([t1, t2, v1, v2, v3])
# db.session.commit()

# vaikai = Vaikas.query.all()
# print(dir(vaikai[0]))
# print(Games.query.filter_by(guesses = 'Opapa').first())
# print(Games.query.filter_by(user_id = 1).all())
# test = Games.query.filter_by(user_id = 1).all()
# list_of_guesses = []
# dict = {}
# for x in test:
#     list_of_guesses.append(x.guesses_made)
#     # print(x.guesses_made)

# for x in list_of_guesses:
#     for i in x:
#         try:
#             dict[i] += 1
#         except:
#             dict[i] = 1
# print(dict)

# test = Games.query.filter_by(user_id = 2).order_by(Games.id.desc()).first()
# test.outcome = 'new2'
# db.session.add(test)
# db.session.commit()
# print(test.outcome)

# import random
# import requests

# # ✅ Random word generator using local file system


# def get_list_of_words(path):
#     with open(path, 'r', encoding='utf-8') as f:
#         return f.read().splitlines()


# words = get_list_of_words('/flask_app/static/dictionary')
# print(words)

# random_word = random.choice(words)
# print(random_word)  # 👉️ sales

# test = "hello"
# dict = {"a": 1, "b": 2, "c": 3}
# print(list(dict.keys())[0])
# print(type(list(dict.keys())[0]))
# print(type(test))
# print(test + list(dict.keys())[0] + str(list(dict.values())[0]))
# print(list(dict.values())[0])


# def from_dictionary_to_string(dict):
#     new_string = ""
#     for x in range(len(dict)):
#         new_string += f"{str(list(dict.keys())[x])}:{str(list(dict.values())[x])} "
#     return new_string


# # print(from_dictionary_to_string(dict))
# print(from_dictionary_to_string(dict))

txt = "Comp1anyX"

x = txt.isalpha()

print(x) 
