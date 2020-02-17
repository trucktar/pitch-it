from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    passhash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(140))

    pitches = db.relationship("Pitch", backref="user", lazy=True)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', bio='{self.bio}')>"

    @property
    def password(self):
        raise AttributeError

    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.passhash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Pitch(db.Model):
    __tablename__ = "pitches"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    upvotes = db.Column(db.Integer, nullable=False, default=0)
    downvotes = db.Column(db.Integer, nullable=False, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f"<Pitch(category='{self.category}', content='{self.content}')>"
