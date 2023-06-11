from app.db import db, BaseModelMixin


class Word(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(40), nullable=False, unique=True)
    meanings = db.relationship('Meaning', backref='word', lazy=False, cascade='all, delete-orphan')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    user_difficulty = db.relationship('Difficulty', backref='word', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, word, meanings, category_id):
        self.word = word
        self.meanings = meanings
        self.category_id = category_id
    
    def __repr__(self):
        return f'Word({self.word})'
    
    def __str__(self):
        return f'{self.word}'
    
    @classmethod
    def get_random(cls, category_id):
        return cls.query.filter_by(category_id=category_id).all().order_by(db.func.random()).first()


class Meaning(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    meaning = db.Column(db.String(80), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    
    def __init__(self, meaning):
        self.meaning = meaning
    
    def __repr__(self):
        return f'Meaning({self.meaning})'
    
    def __str__(self):
        return f'{self.meaning}'