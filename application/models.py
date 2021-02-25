from datetime import datetime
from application import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    description = db.Column(
        db.String(300), nullable=False, default="No description yet."
    )
    questions = db.relationship('Question', backref='author', lazy=True)
    answers = db.relationship('Answer', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Question(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    content = db.Column(db.Text, nullable=False)
    views = db.Column(db.Integer, default=0)
    num_answers = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answers = db.relationship(
        "Answer", backref="title", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Question('{self.title}', '{self.date_posted}')"


class Answer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    answer = db.Column(db.Text, nullable=False)
    question_id = db.Column(
        db.Integer, db.ForeignKey("question.id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Answer('{self.answer}', '{self.date_posted}')"
