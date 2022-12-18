from flask import render_template, redirect, url_for, flash, request, Response
from flask_app import app, db, bcrypt, forms
from flask_login import login_required, current_user, login_user, logout_user
from flask_app.models import User, Game
from flask_app import hangman
import logging
import sqlalchemy

logging.basicConfig(
    filename="hangman_web.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> (Response | str):
    db.create_all()
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("Login failure, please check details", "danger")
    return render_template("login.html", form=form, title="login")


@app.route("/register", methods=["GET", "POST"])
def register() -> (Response | str):
    db.create_all()
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        try:
            encrypted_password = bcrypt.generate_password_hash(
                form.password.data
            ).decode("utf-8")
            user = User(
                name=form.name.data, email=form.email.data, password=encrypted_password
            )
            db.session.add(user)
            db.session.commit()
            flash(f"User: {form.email.data} was successfully created, please log in")
            logging.info(
                f"new account registered: Name - {form.name.data}, Email: {form.email.data}"
            )
            return redirect(url_for("login"))
        except sqlalchemy.exc.IntegrityError as e:
            logging.error(f"Registration failed, reason: {e}")
            flash(f"User: {form.email.data} already in use.", "danger")
            return redirect(url_for("register"))
        except Exception as e:
            logging.error(f"Registration failed, reason: {e}")
            flash(f"Registration failed, please try again laiter.", "danger")
            return redirect(url_for("register"))
    return render_template("register.html", form=form, title="register")


@app.route("/game", methods=["POST"])
@login_required
def game_post() -> str:
    game_from_db = (
        Game.query.filter_by(user_id=current_user.get_id())
        .order_by(Game.id.desc())
        .first()
    )
    user_guess = request.form["guess"].lower()
    if user_guess.isalpha() == False:
        flash(f"Wrong input", "danger")
        return render_template(
            "game.html",
            masked_word=game_from_db.progress,
            visual=f"/static/images/atempt{game_from_db.mistakes}.png",
            counter=game_from_db.mistakes,
            guesses_made=game_from_db.guesses_made,
        )
    if hangman.check_winner(user_guess, game_from_db.word):
        game_from_db.outcome = "won"
        db.session.add(game_from_db)
        db.session.commit()
        return render_template("win.html", secret_word=game_from_db.word)
    if (
        hangman.find_letter_in_string(user_guess, game_from_db.word)
        and hangman.find_letter_in_string(user_guess, game_from_db.guesses_made.lower())
        == False
    ):
        new_progress = hangman.revealing_letters(
            game_from_db.word, game_from_db.progress, user_guess
        )
        game_from_db.progress = new_progress
        game_from_db.guesses_made += user_guess.upper()
        db.session.add(game_from_db)
        db.session.commit()
        if hangman.check_winner(game_from_db.word, game_from_db.progress):
            game_from_db.outcome = "won"
            db.session.add(game_from_db)
            db.session.commit()
            return render_template("win.html", secret_word=game_from_db.word)
        return render_template(
            "game.html",
            masked_word=new_progress,
            visual=f"/static/images/atempt{game_from_db.mistakes}.png",
            counter=game_from_db.mistakes,
            guesses_made=game_from_db.guesses_made,
        )
    if (
        hangman.find_letter_in_string(user_guess, game_from_db.word.lower()) == False
        and hangman.find_letter_in_string(user_guess, game_from_db.guesses_made.lower())
        == False
    ):
        game_from_db.mistakes += 1
        game_from_db.guesses_made += user_guess.upper()
        db.session.add(game_from_db)
        db.session.commit()
        if game_from_db.mistakes >= 10:
            game_from_db.outcome = "lost"
            db.session.add(game_from_db)
            db.session.commit()
            return render_template("loose.html", secret_word=game_from_db.word)
        return render_template(
            "game.html",
            masked_word=game_from_db.progress,
            visual=f"/static/images/atempt{game_from_db.mistakes}.png",
            counter=game_from_db.mistakes,
            guesses_made=game_from_db.guesses_made,
        )
    return render_template(
        "game.html",
        masked_word=game_from_db.progress,
        visual=f"/static/images/atempt{game_from_db.mistakes}.png",
        counter=game_from_db.mistakes,
        guesses_made=game_from_db.guesses_made,
    )


@app.route("/game", methods=["GET"])
@login_required
def game_get() -> str:
    PATH_OF_FUN_WORDS = "flask_app/static/dictionary/positive-words.txt"

    game_from_db = (
        Game.query.filter_by(user_id=current_user.get_id())
        .order_by(Game.id.desc())
        .first()
    )

    if game_from_db and game_from_db.outcome == "In progress":
        masked_word_db = game_from_db.progress
        mistakes = game_from_db.mistakes
        return render_template(
            "game.html",
            masked_word=masked_word_db,
            visual=f"/static/images/atempt{mistakes}.png",
            counter=mistakes,
            guesses_made=game_from_db.guesses_made,
        )

    else:
        random_word = hangman.get_word(PATH_OF_FUN_WORDS)
        masked_word_db = hangman.mask_word(random_word)
        game = Game(
            outcome="In progress",
            word=random_word,
            guesses_made="",
            progress=masked_word_db,
            mistakes=0,
            user_id=current_user.get_id(),
        )
        db.session.add(game)
        db.session.commit()
        return render_template(
            "game.html",
            masked_word=masked_word_db,
            visual="/static/images/atempt0.png",
            counter=0,
        )


@app.route("/stats")
@login_required
def stats() -> str:
    game_from_db = Game.query.filter_by(user_id=current_user.get_id())
    count = len(game_from_db.all())
    won = len(game_from_db.filter_by(outcome="won").all())
    lost = len(game_from_db.filter_by(outcome="lost").all())
    return render_template(
        "stats.html",
        count=count,
        won=won,
        lost=lost,
        guesses=hangman.get_all_guesses_from_db(game_from_db.all()),
    )


@app.route("/logout")
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for("index"))
