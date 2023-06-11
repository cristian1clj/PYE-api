from marshmallow import fields

from app.ext import ma


class CategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    words = fields.Nested('WordSchema', many=True)
    suggestions = fields.Nested('SuggestionSchema', many=True)