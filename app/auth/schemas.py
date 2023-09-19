from marshmallow import fields

from app.ext import ma


class LoginInputSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class LoginOutputSchema(ma.Schema):
    id = fields.Int(required=True)