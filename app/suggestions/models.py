from app.db import db, BaseModelMixin


class Suggestion(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(40), nullable=False)
    meaning = db.Column(db.String(80), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    punctuation = db.Column(db.SmallInteger, nullable=False)
    date_suggestion = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, word, meaning, category_id, user_id, punctuation, date_suggestion):
        self.word = word
        self.meaning = meaning
        self.category_id = category_id
        self.user_id = user_id
        self.punctuation = punctuation
        self.date_suggestion = date_suggestion