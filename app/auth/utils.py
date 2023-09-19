from datetime import datetime, timedelta
import os
import jwt

from ..users.models import User
from config.default import SECRET_KEY


class UserDataAuthentication:
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
            return False