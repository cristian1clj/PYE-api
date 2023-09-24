from flask import request, Blueprint
from flask_restful import Api, Resource

from ..common.error_handling import Conflict
from ..auth.utils import jwt_required
from .schemas import CategorySchema
from .models import Category

CATEGORIES_BP = Blueprint('categories_bp', __name__)

CATEGORY_SCHEMA = CategorySchema()

API = Api(CATEGORIES_BP)


class CategoryListResource(Resource):
    
    def get(self):
        categories = Category.get_all()
        result = CATEGORY_SCHEMA.dump(categories, many=True)
        return result
    
    @jwt_required
    def post(self):
        data = request.get_json()
        category_dict = CATEGORY_SCHEMA.load(data)
        
        existing_category = Category.simple_filter(name=category_dict['name'])
        if existing_category:
            raise Conflict('Category already exists')
        
        category = Category(
            name=category_dict['name']
        )
        category.save()
        
        resp = CATEGORY_SCHEMA.dump(category)
        return resp, 201


API.add_resource(CategoryListResource, '/api/categories/', endpoint='category_list_resource')