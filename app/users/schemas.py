from marshmallow import fields

from app.ext import ma


class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String()
    password = fields.String()
    email = fields.String()
    suggestions = fields.Nested('SuggestionSchema', many=True)
    vocabulary_difficulty = fields.Nested('DifficultySchema', many=True)