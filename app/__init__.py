from flask import Flask, jsonify
from flask_restful import Api

from app.common.error_handling import *
from app.db import db
from app.vocabulary.words.resources import WORDS_BP
from app.vocabulary.difficulty.resources import DIFFICULTY_BP
from app.users.resources import USERS_BP
from app.auth.resources import AUTH_BP
from app.suggestions.resources import SUGGESTIONS_BP
from app.categories.resources import CATEGORIES_BP
from app.ext import ma, migrate


def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)
    
    # Init the extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    
    Api(app, catch_all_404s=True)
    
    app.url_map.strict_slashes = False
    app.register_blueprint(WORDS_BP)
    app.register_blueprint(DIFFICULTY_BP)
    app.register_blueprint(USERS_BP)
    app.register_blueprint(AUTH_BP)
    app.register_blueprint(CATEGORIES_BP)
    app.register_blueprint(SUGGESTIONS_BP)
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        print(e)
        return jsonify({'msg': 'Internal server error'}), 500
    
    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({'msg': 'Method not allowed'}), 405
    
    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({'msg': 'Forbidden error'}), 403
    
    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({'msg': 'Not found error'}), 404
    
    @app.errorhandler(401)
    def handle_401_error(e):
        return jsonify({'msg': 'Unauthorized error'}), 401
    
    @app.errorhandler(AppErrorBaseClass)
    def handle_app_base_error(e):
        return jsonify({'msg': str(e)}), 500
    
    @app.errorhandler(Conflict)
    def handle_conflict_error(e):
        return jsonify({'msg': str(e)}), 409
    
    @app.errorhandler(ObjectNotFound)
    def handle_object_not_found_error(e):
        return jsonify({'msg': str(e)}), 404
    
    @app.errorhandler(Unauthorized)
    def handle_unauthorized_error(e):
        return jsonify({'msg': str(e)}), 401