from flask import Blueprint
from flask_restful import Api

from resources.auth_resources import auth_blueprint, LoginResource, RegisterResource
# from .

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(LoginResource, "/login")
api.add_resource(RegisterResource, "/register")