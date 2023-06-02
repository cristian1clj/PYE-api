from werkzeug.security import generate_password_hash, check_password_hash

from app.db import db, BaseModelMixin


class User(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password_hash = db.Column(db.String)
    email = db.Column(db.String)
    suggestions = db.relationship('Suggestion', backref='user', lazy=True, cascade='all, delete-orphan')
    vocabulary_difficulty = db.relationship('Difficulty', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, username, password, email):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email
    
    def __repr__(self):
        return f'User({self.username})'
    
    def __str__(self):
        return f'{self.username}'
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)