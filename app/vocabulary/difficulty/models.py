from app.db import db, BaseModelMixin


class Difficulty(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    difficulty_level = db.Column(db.Integer)
    
    def __init__(self, user_id, word_id, difficulty_level):
        self.user_id = user_id
        self.word_id = word_id
        self.difficulty_level = difficulty_level