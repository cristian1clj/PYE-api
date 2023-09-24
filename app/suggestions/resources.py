from datetime import datetime

from flask import request, Blueprint
from flask_restful import Api, Resource

from ..common.error_handling import ObjectNotFound
from ..auth.utils import DataAuthentication, jwt_required
from .schemas import SuggestionSchema
from .models import Suggestion
from ..categories.models import Category
from ..users.models import User

SUGGESTIONS_BP = Blueprint('suggestions_bp', __name__)

SUGGESTION_SCHEMA = SuggestionSchema()

API = Api(SUGGESTIONS_BP)


class SuggestionListResource(Resource):
    
    @jwt_required
    def get(self):
        suggestions = Suggestion.get_all()
        result = SUGGESTION_SCHEMA.dump(suggestions, many=True)
        return result
    
    @jwt_required
    def post(self, current_user):
        data = request.get_json()
        suggestion_dict = SUGGESTION_SCHEMA.load(data, partial=True)
        
        DataAuthentication.check_access_by_id(
            suggestion_dict['user_id'], 
            current_user['id']
            )
        
        user = User.get_by_id(suggestion_dict['user_id'])
        if user is None:
            raise ObjectNotFound('The user does not exist')
        
        category = Category.get_by_id(suggestion_dict['category_id'])
        if category is None:
            raise ObjectNotFound('The category does not exist')
        
        suggestion = Suggestion(
            word=suggestion_dict['word'],
            meaning=suggestion_dict['meaning'],
            category_id=suggestion_dict['category_id'],
            user_id=suggestion_dict['user_id'],
            punctuation=0,
            date_suggestion=datetime.now()
        )
        suggestion.save()
        
        resp = SUGGESTION_SCHEMA.dump(suggestion)
        return resp, 201
    
    
class SuggestionResource(Resource):
    
    def _suggestion_validation(self, suggestion_id):
        suggestion = Suggestion.get_by_id(suggestion_id)
        if suggestion is None:
            raise ObjectNotFound('The suggestion does not exist')
        
        return suggestion
    
    @jwt_required
    def get(self, suggestion_id):
        suggestion = self._suggestion_validation(suggestion_id)
        resp = SUGGESTION_SCHEMA.dump(suggestion)
        return resp
    
    @jwt_required
    def put(self, suggestion_id, current_user):
        suggestion = self._suggestion_validation(suggestion_id)
        
        DataAuthentication.check_access_by_id(suggestion.user_id, current_user['id'])
        
        data = request.get_json()
        suggestion_dict = SUGGESTION_SCHEMA.load(data)
        
        user = User.get_by_id(suggestion_dict['user_id'])
        if user is None:
            raise ObjectNotFound('The user does not exist')
        
        category = Category.get_by_id(suggestion_dict['category_id'])
        if category is None:
            raise ObjectNotFound('The category does not exist')
        
        suggestion.word = suggestion_dict['word']
        suggestion.meaning = suggestion_dict['meaning']
        suggestion.category_id = suggestion_dict['category_id']
        suggestion.user_id = suggestion_dict['user_id']
        suggestion.punctuation = suggestion_dict['punctuation']
        suggestion.update()
        
        resp = SUGGESTION_SCHEMA.dump(suggestion)
        return resp
    
    @jwt_required
    def delete(self, suggestion_id, current_user):
        suggestion = self._suggestion_validation(suggestion_id)
        DataAuthentication.check_access_by_id(suggestion.user_id, current_user['id'])
        suggestion.delete()
        return {"message": "Suggestion deleted"}


API.add_resource(SuggestionListResource, '/api/suggestions/', endpoint='suggestion_list_resource')
API.add_resource(SuggestionResource, '/api/suggestions/<int:suggestion_id>', endpoint='suggestion_resource')