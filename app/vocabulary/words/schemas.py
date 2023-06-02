from marshmallow import fields

from app.ext import ma


class WordSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    word = fields.String(required=True)
    meanings = fields.Nested('MeaningSchema', many=True)
    user_difficulty = fields.Nested('DifficultySchema', many=True)


class MeaningSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    meaning = fields.String(required=True)