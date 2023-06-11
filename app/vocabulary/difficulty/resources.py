from flask import request, Blueprint
from flask_restful import Api, Resource

from ...common.error_handling import ObjectNotFound
from .schemas import DifficultySchema
from .models import Difficulty
from ...users.models import User
from ..words.models import Word

difficulty_bp = Blueprint('difficulty_bp', __name__)

difficulty_schema = DifficultySchema()

api = Api(difficulty_bp)


class DifficultyListResource(Resource):
    def get(self):
        words = Difficulty.get_all()
        result = difficulty_schema.dump(words, many=True)
        return result
    
    def post(self):
        data = request.get_json()
        difficulty_dict = difficulty_schema.load(data)
        
        word_id = difficulty_dict.get('word_id')
        word = Word.get_by_id(word_id)
        if word is None:
            raise ObjectNotFound('The word does not exist')
        
        user_id = difficulty_dict.get('user_id')
        user = User.get_by_id(user_id)
        if user is None:
            raise ObjectNotFound('The user does not exist')
        
        difficulty = Difficulty(
            word_id=difficulty_dict['word_id'],
            user_id=difficulty_dict['user_id'],
            difficulty_level=difficulty_dict['difficulty_level']
        )
        difficulty.save()
        resp = difficulty_schema.dump(difficulty)
        return resp, 201


class DifficultyResource(Resource):
    def _validate_user_word_difficulty(self, user_id, word_id):
        user = User.get_by_id(user_id)
        if user is None:
            raise ObjectNotFound('The user does not exist')
        word = Word.get_by_id(word_id)
        if word is None:
            raise ObjectNotFound('The word does not exist')
        
        difficulty = Difficulty.simple_filter(user_id=user_id, word_id=word_id)
        if difficulty is None:
            raise ObjectNotFound("Difficulty not found for this word and this user")
        
        return difficulty
    
    def get(self, user_id, word_id):
        difficulty = self._validate_user_word_difficulty(user_id, word_id)
        result = difficulty_schema.dump(difficulty)
        return result
    
    def put(self, user_id, word_id):
        difficulty = self._validate_user_word_difficulty(user_id, word_id)

        data = request.get_json()
        difficulty.user_id = data['user_id']
        difficulty.word_id = data['word_id']
        difficulty.difficulty_level = data['difficulty_level']
        difficulty.update()
        
        resp = difficulty_schema.dump(difficulty)
        return resp
    
    def delete(self, user_id, word_id):
        difficulty = self._validate_user_word_difficulty(user_id, word_id)
        difficulty.delete()
        return {"message": "Difficulty deleted"}, 204
    

api.add_resource(DifficultyListResource, '/api/vocabulary/difficulty/', endpoint='difficulty_list_resource')
api.add_resource(DifficultyResource, '/api/vocabulary/difficulty/user/<int:user_id>/word/<int:word_id>', endpoint='difficulty_resource')