from flask import Blueprint, jsonify, request, current_app
from flask_security.utils import verify_password, hash_password
import datetime
from flask_restful import Resource, marshal, fields, marshal_with, reqparse

from models import *
from .marshal_fields import user_fields
from services.user_service import UserService

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/auth')

# @auth_blueprint.route('/login', methods = ['POST'])
# def login():
    # data = request.get_json()
    # user_name = data['user_name']
    # password = data['user_password']

    # if (not user_name or not password):
    #     return jsonify({'message': 'invalid input'}), 400
    
    # user = User.query.filter(User.user_name == user_name).first()

    # if not verify_password(password, user.user_password):
    #     return jsonify({'message':'Wrong password or username'}), 400

    # return jsonify(
    #     {
    #         'user_id': user.user_id,
    #         'user_name': user.user_name,
    #         'token': user.get_auth_token(),
    #         'role':user.roles[0].name
    #     }
    # ), 200

parser = reqparse.RequestParser()
parser.add_argument("user_name", type = str, required = True)
parser.add_argument("user_password", type = str, required = True)
parser.add_argument("email", type = str)
parser.add_argument("contact_number", type = str)

marshal_fields = user_fields
service = UserService

class LoginResource(Resource):
    # @marshal_with(user_fields)
    def post(self):
        args = parser.parse_args()
        user_name = args.get("user_name")
        user_password = args.get("user_password")

        user = User.query.filter(User.user_name == user_name).first()
        if not verify_password(user_password, user.user_password):
            return 400        
        return marshal(user, user_fields), 200

class RegisterResource(Resource):
    def post(self):
        args = parser.parse_args()
        user_name = args.get("user_name")
        user_password = args.get("user_password")
        email = args.get("email")
        contact_number = args.get("contact_number")

        datastore = current_app.datastore
        # user = datastore.find_user(user_name = user_name)

        user = datastore.create_user(user_name = user_name, user_password = hash_password(user_password), 
                          contact_number = contact_number, email = email)
        
        datastore.add_role_to_user(user, 'Patient')
        db.session.commit()

        return marshal(user, user_fields), 200

@auth_blueprint.route('/register', methods = ['POST'])
def register():
    data = request.get_json()

    # User table required fields
    user_name = data['user_name']
    user_password = data['user_password']
    contact_number = data['contact_number']
    email = data['email']

    # Patient table required fields
    name = data['name']
    gender = data['gender']
    dob = data['dob']
    height = data['height']
    weight = data['weight']

    datastore = current_app.datastore
    user = datastore.find_user(user_name = user_name)

    # check if this user already exists
    if user:
        return jsonify({'message': 'Already exists'}), 400
    
    # add as user
    user = datastore.create_user(user_name = user_name, user_password = hash_password(user_password), 
                          contact_number = contact_number, email = email)
    # add as patient
    user.user_patient = Patient(name = name, gender = gender, dob = datetime.strptime(dob, '%Y/%m/%d'), 
                                height = height, weight = weight)
    # assign role
    datastore.add_role_to_user(user, 'Patient')

    db.session.commit()

    return jsonify(
        {
            'user_name': user.user_name,
            'contact_number': user.contact_number,
            'email': user.email,
            'name':user.user_patient.name
        }
    ), 201

# use marshal, req_parse