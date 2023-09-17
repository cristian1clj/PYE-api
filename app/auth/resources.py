from flask import request, Blueprint
from flask_restful import Api, Resource

from ..common.error_handling import ObjectNotFound
from ..users.schemas import UserSchema
from ..users.models import User
from .schemas import LoginInputSchema, LoginOutputSchema
from .utils import LoginAuthentication, TokenGenerator

auth_bp = Blueprint('auth_bp', __name__)

api = Api(auth_bp)


class RegistrationResource(Resource):
    def post(self):
        user_schema = UserSchema()
        
        data = request.get_json()
        user_dict = user_schema.load(data)
        user = User(
            username=user_dict['username'],
            password=user_dict['password'],
            email=user_dict['email']
        )
        user.save()
        resp = user_schema.dump(user)
        return resp, 201


class AuthenticationResource(Resource):
    def post(self):
        login_input_schema = LoginInputSchema()
        
        data = request.get_json()
        account_dict = login_input_schema.load(data)
        email = account_dict.get('email')
        password = account_dict.get('password')
        
        user = LoginAuthentication.check_user_exists(email)
        if user is None:
            raise ObjectNotFound("User not found")
        
        if user.check_password(password):
            token = TokenGenerator.encode_token(user)
            resp = { "token": token }
            return resp
        

api.add_resource(AuthenticationResource, '/api/auth/login', endpoint='authentication_resource')