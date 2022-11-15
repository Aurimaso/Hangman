from flask_app import app, db, bcrypt, forms
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from flask_app.models import User
from datetime import datetime, timedelta
import requests

@app.route("/")
def index():
    # if current_user.is_authenticated:
    #     print(current_user.id)
    # else:
    #     print("not authenticated")
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    db.create_all()
    # if current_user.is_authenticated:
    #     return redirect(url_for("index"))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            if current_user.is_authenticated:
                print(current_user)
            else:
                print("no current user")
            next_page = request.args.get("next")
            print("login successful")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("Login failure, please check details", "danger")
    return render_template("login.html", form=form, title="login")


@app.route("/register", methods=["GET", "POST"])
def register():
    db.create_all()
    # if current_user.is_authenticated:
    #     return redirect(url_for("index"))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            name=form.name.data, email=form.email.data, password=encrypted_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f"User: {form.email.data} was successfully created, please log in")
        return redirect(url_for("login"))
    return render_template("register.html", form=form, title="register")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
