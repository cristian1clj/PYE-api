from datetime import datetime

from flask import request, Blueprint
from flask_restful import Api, Resource

from ..common.error_handling import ObjectNotFound
from .schemas import SuggestionSchema
from .models import Suggestion
from ..categories.models import Category
from ..users.models import User

suggestions_bp = Blueprint('suggestions_bp', __name__)

suggestion_schema = SuggestionSchema()

api = Api(suggestions_bp)


class SuggestionListResource(Resource):
    def get(self):
        suggestions = Suggestion.get_all()
        result = suggestion_schema.dump(suggestions, many=True)
        return result
    
    def post(self):
        data = request.get_json()
        suggestion_dict = suggestion_schema.load(data, partial=True)
        
        category_id = suggestion_dict.get('category_id')
        category = Category.get_by_id(category_id)
        if category is None:
            raise ObjectNotFound('The category does not exist')
        
        user_id = suggestion_dict.get('user_id')
        user = User.get_by_id(user_id)
        if user is None:
            raise ObjectNotFound('The user does not exist')
        
        suggestion = Suggestion(
            word=suggestion_dict['word'],
            meaning=suggestion_dict['meaning'],
            category_id=category_id,
            user_id=user_id,
            punctuation=0,
            date_suggestion=datetime.now()
        )
        suggestion.save()
        resp = suggestion_schema.dump(suggestion)
        return resp, 201
    
    
class SuggestionResource(Resource):
    def _suggestion_validation(self, suggestion_id):
        suggestion = Suggestion.get_by_id(suggestion_id)
        if suggestion is None:
            raise ObjectNotFound('The suggestion does not exist')
        
        return suggestion
    
    def get(self, suggestion_id):
        suggestion = self._suggestion_validation(suggestion_id)
        resp = suggestion_schema.dump(suggestion)
        return resp
    
    def put(self, suggestion_id):
        suggestion = self._suggestion_validation(suggestion_id)

        data = request.get_json()
        suggestion.word = data['word']
        suggestion.meaning = data['meaning']
        suggestion.category_id = data['category_id']
        suggestion.user_id = data['user_id']
        suggestion.punctuation = data['punctuation']
        suggestion.update()
        
        resp = suggestion_schema.dump(suggestion)
        return resp
    
    def delete(self, suggestion_id):
        suggestion = self._suggestion_validation(suggestion_id)
        suggestion.delete()
        return {"message": "Suggestion deleted"}


api.add_resource(SuggestionListResource, '/api/suggestions/', endpoint='suggestion_list_resource')
api.add_resource(SuggestionResource, '/api/suggestions/<int:suggestion_id>', endpoint='suggestion_resource')