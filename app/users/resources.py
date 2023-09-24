from flask import request, Blueprint
from flask_restful import Api, Resource

from ..common.error_handling import ObjectNotFound
from ..auth.utils import DataAuthentication, jwt_required
from .schemas import UserSchema
from .models import User

USERS_BP = Blueprint('users_bp', __name__)

USER_SCHEMA = UserSchema()

API = Api(USERS_BP)


class UserListResource(Resource):
    
    @jwt_required
    def get(self):
        users = User.get_all()
        result = USER_SCHEMA.dump(users, many=True)
        return result


class UserResource(Resource):
    
    def _user_validation(self, user_id, current_id):
        DataAuthentication.check_access_by_id(user_id, current_id)
        
        user = User.get_by_id(user_id)
        if user is None:
            raise ObjectNotFound("User not found")
        
        return user
    
    @jwt_required
    def get(self, user_id, current_user):
        user = self._user_validation(user_id, current_user['id'])
        resp = USER_SCHEMA.dump(user)
        return resp
    
    @jwt_required
    def put(self, user_id, current_user):
        user = self._user_validation(user_id, current_user['id'])

        data = request.get_json()
        # user_dict = USER_SCHEMA.load(data)
        user.username = data['username']
        user.email = data['email']
        user.update()
        
        resp = USER_SCHEMA.dump(user)
        return resp
    
    @jwt_required
    def delete(self, user_id, current_user):
        user = self._user_validation(user_id, current_user['id'])
        user.delete()
        return {"message": "User deleted"}


API.add_resource(UserListResource, '/api/users/', endpoint='user_list_resource')
API.add_resource(UserResource, '/api/users/<int:user_id>', endpoint='user_resource')