from marshmallow import fields

from app.ext import ma


class SuggestionSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    word = fields.String(required=True)
    meaning = fields.String(required=True)
    category_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    punctuation = fields.Integer(default=0, missing=0)
    date_suggestion = fields.DateTime()