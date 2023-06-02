from app.db import db, BaseModelMixin


class Category(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    suggestions = db.relationship('Suggestion', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f'Category({self.name})'
    
    def __str__(self):
        return f'{self.name}'