from flask import request, Blueprint
from flask_restful import Api, Resource

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
        word = Word(
            word=word_dict['word'],
            meanings=[Meaning(meaning['meaning']) for meaning in word_dict['meanings']]
        )
        word.save()
        resp = word_schema.dump(word)
        return resp, 201


class WordRandomResource(Resource):
    def get(self):
        word = Word.get_random()
        result = word_schema.dump(word)
        return result


api.add_resource(WordListResource, '/api/vocabulary/', endpoint='word_list_resource')
api.add_resource(WordRandomResource, '/api/vocabulary/random', endpoint='word_random_resource')