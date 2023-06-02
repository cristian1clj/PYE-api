from flask import request, Blueprint
from flask_restful import Api, Resource

from .schemas import UserSchema
from .models import User

users_bp = Blueprint('users_bp', __name__)

user_schema = UserSchema()

api = Api(users_bp)


class UserListResource(Resource):
    def get(self):
        users = User.get_all()
        result = user_schema.dump(users, many=True)
        return result
    
    def post(self):
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


api.add_resource(UserListResource, '/api/users/', endpoint='user_list_resource')