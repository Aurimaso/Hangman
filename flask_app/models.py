from flask_app import db
from sqlalchemy import DateTime
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String(50))
    email = db.Column("Email", db.String(180), unique=True, nullable=False)
    password = db.Column("Password", db.String(100), nullable=False)