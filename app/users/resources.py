from flask import request, Blueprint
from flask_restful import Api, Resource

from ..common.error_handling import ObjectNotFound
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


class UserResource(Resource):
    def _user_validation(self, user_id):
        user = User.get_by_id(user_id)
        if user is None:
            raise ObjectNotFound("User not found")
        
        return user
    
    def get(self, user_id):
        user = self._user_validation(user_id)
        resp = user_schema.dump(user)
        return resp
    
    def put(self, user_id):
        user = self._user_validation(user_id)

        data = request.get_json()
        user.username = data['username']
        user.email = data['email']
        user.update()
        
        resp = user_schema.dump(user)
        return resp
    
    def delete(self, user_id):
        user = self._user_validation(user_id)
        user.delete()
        return {"message": "User deleted"}


api.add_resource(UserListResource, '/api/users/', endpoint='user_list_resource')
api.add_resource(UserResource, '/api/users/<int:user_id>', endpoint='user_resource')