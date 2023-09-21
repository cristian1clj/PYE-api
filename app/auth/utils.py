from datetime import datetime, timedelta
from inspect import signature
from functools import wraps
import jwt

from flask import request

from ..common.error_handling import Unauthorized
from ..users.models import User
from config.default import SECRET_KEY


class DataAuthentication:
    
    @staticmethod
    def is_jwt_provided():
        token = request.headers.get('Authorization')
        if not token:
            raise Unauthorized('Token not provided')
        return token
    
    @staticmethod
    def check_access_by_id(id_query, current_user_id):
        if id_query is not current_user_id:
            raise Unauthorized('User ID provided does not match the current session')
    
    @staticmethod
    def check_email_exists(email):
        return User.query.filter_by(email=email).first()


class TokenGenerator:
    
    @staticmethod
    def encode_token(user):
        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token
    
    @staticmethod
    def decode_token(token):
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms='HS256',
            options={"require_exp": True}
        )
    
    @staticmethod
    def check_token(token):
        try:
            jwt.decode(
                token,
                SECRET_KEY,
                algorithms='HS256',
                options={"require_exp": True}
            )
            return True
        except:
            raise Unauthorized('Invalid token')
    
    @staticmethod
    def check_token_user(token):
        try:
            return jwt.decode(
                token,
                SECRET_KEY,
                algorithms='HS256',
                options={"require_exp": True}
            )
        except:
            raise Unauthorized('Invalid token')


def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = DataAuthentication.is_jwt_provided()
        token = token.replace('Bearer ', '')
        
        if 'current_user' in signature(fn).parameters:
            user = TokenGenerator.check_token_user(token)
            
            current_user = {
                'id': user['id']
            }
            kwargs['current_user'] = current_user
            return fn(*args, **kwargs)
        
        else:
            TokenGenerator.check_token(token)
            return fn(*args, **kwargs)
    return wrapper