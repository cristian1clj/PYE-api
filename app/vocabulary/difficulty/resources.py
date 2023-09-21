from flask import request, Blueprint
from flask_restful import Api, Resource

from ...common.error_handling import ObjectNotFound, Conflict
from ...auth.utils import DataAuthentication, jwt_required
from .schemas import DifficultySchema
from .models import Difficulty
from ...users.models import User
from ..words.models import Word

difficulty_bp = Blueprint('difficulty_bp', __name__)

difficulty_schema = DifficultySchema()

api = Api(difficulty_bp)


class DifficultyListResource(Resource):
    
    @jwt_required
    def get(self):
        words = Difficulty.get_all()
        result = difficulty_schema.dump(words, many=True)
        return result
    
    @jwt_required
    def post(self, current_user):
        data = request.get_json()
        difficulty_dict = difficulty_schema.load(data)
        
        DataAuthentication.check_access_by_id(
            difficulty_dict['user_id'], 
            current_user['id']
            )
        
        user = User.get_by_id(difficulty_dict['user_id'])
        if user is None:
            raise ObjectNotFound('The user does not exist')
        
        word = Word.get_by_id(difficulty_dict['word_id'])
        if word is None:
            raise ObjectNotFound('The word does not exist')
        
        existing_difficulty = Difficulty.get_difficulty(
            difficulty_dict['user_id'], 
            difficulty_dict['word_id']
            )
        if existing_difficulty:
            raise Conflict('Difficulty already exists')

        difficulty = Difficulty(
            word_id=difficulty_dict['word_id'],
            user_id=difficulty_dict['user_id'],
            difficulty_level=difficulty_dict['difficulty_level']
        )
        difficulty.save()
        
        resp = difficulty_schema.dump(difficulty)
        return resp, 201


class DifficultyResource(Resource):
    def _validate_user_word_difficulty(self, user_id, word_id, current_id):
        DataAuthentication.check_access_by_id(user_id, current_id)
        
        user = User.get_by_id(user_id)
        if user is None:
            raise ObjectNotFound('The user does not exist')
        
        word = Word.get_by_id(word_id)
        if word is None:
            raise ObjectNotFound('The word does not exist')
        
        difficulty = Difficulty.get_difficulty(user_id, word_id)
        if difficulty is None:
            raise ObjectNotFound("Difficulty not found for this word and this user")
        
        return difficulty
    
    @jwt_required
    def get(self, user_id, word_id, current_user):
        difficulty = self._validate_user_word_difficulty(
            user_id, 
            word_id, 
            current_user['id']
            )
        
        result = difficulty_schema.dump(difficulty)
        return result
    
    @jwt_required
    def put(self, user_id, word_id, current_user):
        difficulty = self._validate_user_word_difficulty(
            user_id, 
            word_id, 
            current_user['id']
            )

        data = request.get_json()
        # difficulty_dict = difficulty_schema.load(data)
        difficulty.difficulty_level = data['difficulty_level']
        difficulty.update()
        
        resp = difficulty_schema.dump(difficulty)
        return resp
    
    @jwt_required
    def delete(self, user_id, word_id, current_user):
        difficulty = self._validate_user_word_difficulty(
            user_id, 
            word_id, 
            current_user['id']
            )
        difficulty.delete()
        return {"message": "Difficulty deleted"}
    

api.add_resource(DifficultyListResource, '/api/vocabulary/difficulty/', endpoint='difficulty_list_resource')
api.add_resource(DifficultyResource, '/api/vocabulary/difficulty/user/<int:user_id>/word/<int:word_id>', endpoint='difficulty_resource')