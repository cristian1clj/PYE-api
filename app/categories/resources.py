from flask import request, Blueprint
from flask_restful import Api, Resource

from ..common.error_handling import Conflict
from ..auth.utils import jwt_required
from .schemas import CategorySchema
from .models import Category

categories_bp = Blueprint('categories_bp', __name__)

category_schema = CategorySchema()

api = Api(categories_bp)


class CategoryListResource(Resource):
    
    def get(self):
        categories = Category.get_all()
        result = category_schema.dump(categories, many=True)
        return result
    
    @jwt_required
    def post(self):
        data = request.get_json()
        category_dict = category_schema.load(data)
        
        existing_category = Category.simple_filter(name=category_dict['name'])
        if existing_category:
            raise Conflict('Category already exists')
        
        category = Category(
            name=category_dict['name']
        )
        category.save()
        
        resp = category_schema.dump(category)
        return resp, 201


api.add_resource(CategoryListResource, '/api/categories/', endpoint='category_list_resource')