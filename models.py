from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="viewer"
    )
class Bureau(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)

    rates = db.relationship(
        "ExchangeRate",
        backref="bureau",
        lazy=True
    )


class ExchangeRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    buy_rate = db.Column(db.Float, nullable=False)
    sell_rate = db.Column(db.Float, nullable=False)

    recorded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    bureau_id = db.Column(
        db.Integer,
        db.ForeignKey("bureau.id"),
        nullable=False
    )