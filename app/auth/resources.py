from flask import request, Blueprint
from flask_restful import Api, Resource

from ..common.error_handling import ObjectNotFound, Unauthorized, Conflict
from ..users.schemas import UserSchema
from ..users.models import User
from .schemas import LoginInputSchema
from .utils import DataAuthentication, TokenGenerator

AUTH_BP = Blueprint('auth_bp', __name__)

API = Api(AUTH_BP)


class RegistrationResource(Resource):
    
    def post(self):
        USER_SCHEMA = UserSchema()
        
        data = request.get_json()
        user_dict = USER_SCHEMA.load(data)
        
        existing_email = DataAuthentication.check_email_exists(user_dict['email'])
        if existing_email:
            raise Conflict('Email already exists')
        
        user = User(
            username=user_dict['username'],
            password=user_dict['password'],
            email=user_dict['email']
        )
        user.save()
        
        resp = USER_SCHEMA.dump(user)
        return resp, 201


class AuthenticationResource(Resource):
    
    def post(self):
        LOGIN_INPUT_SCHEMA = LoginInputSchema()
        
        data = request.get_json()
        account_dict = LOGIN_INPUT_SCHEMA.load(data)
        
        user = DataAuthentication.check_email_exists(account_dict['email'])
        if user is None:
            raise ObjectNotFound("User not found")
        
        if user.check_password(account_dict['password']):
            token = TokenGenerator.encode_token(user)
            resp = { "token": token }
            return resp
        
        else:
            raise Unauthorized('Invalid password')


class ActiveSessionResource(Resource):
    
    def get(self):
        try:
            token = request.headers.get('Authorization')
            token = token.replace('Bearer ', '')
            return TokenGenerator.check_token(token)
        except:
            return False


API.add_resource(RegistrationResource, '/api/auth/signup', endpoint='registration_resource')
API.add_resource(AuthenticationResource, '/api/auth/login', endpoint='authentication_resource')
API.add_resource(ActiveSessionResource, '/api/auth/session', endpoint='active_session_resource')