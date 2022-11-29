from flask_app import app, db, bcrypt, forms
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from flask_app.models import User, Game
from flask_app import hangman
import logging

logging.basicConfig(filename='hangman_web.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
logging.basicConfig(filename='hangman_web.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')


@app.route("/")
def index() -> str:
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    db.create_all()
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            print("login successful")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("Login failure, please check details", "danger")
    return render_template("login.html", form=form, title="login")


@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    db.create_all()
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        try:
            encrypted_password = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )
            user = User(
                name=form.name.data, email=form.email.data, password=encrypted_password
            )
            db.session.add(user)
            db.session.commit()
            flash(f"User: {form.email.data} was successfully created, please log in")
            logging.info(f"new account registered: Name - {form.name.data}, Email: {form.email.data}")
            return redirect(url_for("login"))
        except Exception as e:
            logging.error(f"Registration failed, reason: {e}")
            flash(f"User: {form.email.data} already in use", "danger")
            return redirect(url_for("register"))
    return render_template("register.html", form=form, title="register")

@app.route("/game", methods=["POST"])
@login_required
def game_post() -> str:
    game_from_db = Game.query.filter_by(user_id = current_user.get_id()).order_by(Game.id.desc()).first()
    letter = request.form["content"].lower()
    if hangman.letter_in_word(letter, game_from_db.guesses_made.lower()) == False:
        game_from_db.guesses_made += letter.upper()
    if hangman.letter_in_word(letter, game_from_db.word):
        new_progress = hangman.revealing_letters(game_from_db.word, game_from_db.progress, letter)
        game_from_db.progress = new_progress
        db.session.add(game_from_db)
        db.session.commit()
        if hangman.check_winner(game_from_db.word, game_from_db.progress):
            game_from_db.outcome = 'won'
            db.session.add(game_from_db)
            db.session.commit()
            return render_template('win.html')
        return render_template('game.html', masked_word= new_progress, tries=f"/static/images/atempt{game_from_db.mistakes}.png", counter = game_from_db.mistakes, guesses_made = game_from_db.guesses_made)
    if hangman.letter_in_word(letter, game_from_db.word) == False:
        game_from_db.mistakes += 1
        db.session.add(game_from_db)
        db.session.commit()
        if game_from_db.mistakes >= 10:
            game_from_db.outcome = 'lost'
            db.session.add(game_from_db)
            db.session.commit()
            return render_template('lost.html')
        return render_template('game.html', masked_word= game_from_db.progress, tries=f"/static/images/atempt{game_from_db.mistakes}.png", counter = game_from_db.mistakes, guesses_made = game_from_db.guesses_made)
    
@app.route("/game", methods=["GET"])
@login_required
def game_get() -> str:
    game_from_db = Game.query.filter_by(user_id = current_user.get_id()).order_by(Game.id.desc()).first()
    PATH_OF_FUN_WORDS = "flask_app/static/dictionary/positive-words.txt"
    try:
        if game_from_db.outcome == 'In progress':
            masked_word_db = game_from_db.progress
            mistakes = game_from_db.mistakes
        return render_template('game.html', masked_word = masked_word_db, tries=f"/static/images/atempt{mistakes}.png", counter = mistakes, guesses_made = game_from_db.guesses_made)

    except:
        random_word = hangman.get_word(PATH_OF_FUN_WORDS)
        masked_word_db = hangman.masking_word(random_word)
        game = Game('In progress', random_word, '', masked_word_db, 0, current_user.get_id())
        db.session.add(game)
        db.session.commit()
        return render_template('game.html', masked_word = masked_word_db, tries="/static/images/atempt0.png", counter = 0)

@app.route("/stats")
@login_required
def stats() -> str:
    game_from_db = Game.query.filter_by(user_id = current_user.get_id())
    count = len(game_from_db.all())
    won = len(game_from_db.filter_by(outcome = 'won').all())
    lost = len(game_from_db.filter_by(outcome = 'lost').all())
    return render_template('stats.html', count = count, won = won, lost = lost, guesses = hangman.from_dictionary_to_string(hangman.get_all_guesses_from_db(game_from_db)))

@app.route("/logout")
@login_required
def logout() -> str:
    logout_user()
    return redirect(url_for("index"))
