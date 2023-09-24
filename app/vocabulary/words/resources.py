from flask import request, Blueprint
from flask_restful import Api, Resource

from ...common.error_handling import ObjectNotFound, Conflict
from ...categories.models import Category
from ...auth.utils import jwt_required
from .schemas import WordSchema
from .models import Word, Meaning

WORDS_BP = Blueprint('words_bp', __name__)

WORD_SCHEMA = WordSchema()

API = Api(WORDS_BP)


class WordListResource(Resource):
    
    def get(self):
        words = Word.get_all()
        result = WORD_SCHEMA.dump(words, many=True)
        return result
    
    @jwt_required
    def post(self):
        data = request.get_json()
        word_dict = WORD_SCHEMA.load(data)
        
        existing_word = Word.simple_filter(word=word_dict['word'])
        if existing_word:
            raise Conflict('Word already exists')
        
        category = Category.get_by_id(word_dict['category_id'])
        if category is None:
            raise ObjectNotFound('The category does not exist')
        
        word = Word(
            word=word_dict['word'],
            meanings=[Meaning(meaning['meaning']) for meaning in word_dict['meanings']],
            category_id=word_dict['category_id']
        )
        word.save()
        
        resp = WORD_SCHEMA.dump(word)
        return resp, 201


class WordResource(Resource):
    
    def _word_validation(self, word_id):
        word = Word.get_by_id(word_id)
        if word is None:
            raise ObjectNotFound("Word not found")
        
        return word
    
    @jwt_required
    def get(self, word_id):
        word = self._word_validation(word_id)
        resp = WORD_SCHEMA.dump(word)
        return resp
    
    @jwt_required
    def put(self, word_id):
        word = self._word_validation(word_id)
        
        data = request.get_json()
        word_dict = WORD_SCHEMA.load(data)
        
        word.word = word_dict['word']
        word.meanings = [Meaning(meaning['meaning']) for meaning in word_dict['meanings']]
        word.category_id = word_dict['category_id']
        word.update()
        
        resp = WORD_SCHEMA.dump(word)
        return resp
    
    @jwt_required
    def delete(self, word_id):
        word = self._word_validation(word_id)
        word.delete()
        return {"message": "Word deleted"}


class WordRandomResource(Resource):
    
    @jwt_required
    def get(self, category_id):
        category = Category.get_by_id(category_id)
        if category is None:
            raise ObjectNotFound('The category does not exist')
        
        word = Word.get_random(category_id)
        result = WORD_SCHEMA.dump(word)
        return result


API.add_resource(WordListResource, '/api/vocabulary/', endpoint='word_list_resource')
API.add_resource(WordResource, '/api/vocabulary/word/<int:word_id>', endpoint='word_resource')
API.add_resource(WordRandomResource, '/api/vocabulary/category/<int:category_id>/random', endpoint='word_random_resource')