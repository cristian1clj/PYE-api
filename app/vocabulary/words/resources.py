from flask import request, Blueprint
from flask_restful import Api, Resource

from ...common.error_handling import ObjectNotFound
from ...categories.models import Category
from .schemas import WordSchema
from .models import Word, Meaning

words_bp = Blueprint('words_bp', __name__)

word_schema = WordSchema()

api = Api(words_bp)


class WordListResource(Resource):
    def get(self):
        words = Word.get_all()
        result = word_schema.dump(words, many=True)
        return result
    
    def post(self):
        data = request.get_json()
        word_dict = word_schema.load(data)
        
        category_id = word_dict.get('category_id')
        category = Category.get_by_id(category_id)
        if category is None:
            raise ObjectNotFound('The category does not exist')
        
        word = Word(
            word=word_dict['word'],
            meanings=[Meaning(meaning['meaning']) for meaning in word_dict['meanings']],
            category_id=category_id
        )
        word.save()
        resp = word_schema.dump(word)
        return resp, 201


class WordResource(Resource):
    def _word_validation(self, word_id):
        word = Word.get_by_id(word_id)
        if word is None:
            raise ObjectNotFound("Word not found")
        
        return word
    
    def get(self, word_id):
        word = self._word_validation(word_id)
        resp = word_schema.dump(word)
        return resp
    
    def put(self, word_id):
        word = self._word_validation(word_id)
        
        data = request.get_json()
        word.word = data['word']
        word.meanings = data['meaning']
        word.category_id = data['category_id']
        word.update()
        
        resp = word_schema.dump(word)
        return resp
    
    def delete(self, word_id):
        word = self._word_validation(word_id)
        word.delete()
        return {"message": "Word deleted"}, 204


class WordRandomResource(Resource):
    def get(self, category_id):
        word = Word.get_random(category_id)
        result = word_schema.dump(word)
        return result


api.add_resource(WordListResource, '/api/vocabulary/', endpoint='word_list_resource')
api.add_resource(WordResource, 'api/vocabulary/word/<int:word_id>', endpoint='word_resource')
api.add_resource(WordRandomResource, '/api/vocabulary/category/<int:category_id>/random', endpoint='word_random_resource')