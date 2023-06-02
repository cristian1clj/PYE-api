from marshmallow import fields

from app.ext import ma


class DifficultySchema(ma.Schema):
    user_id = fields.Integer(required=True)
    word_id = fields.Integer(required=True)
    difficulty_level = fields.Integer(default=5, missing=5)