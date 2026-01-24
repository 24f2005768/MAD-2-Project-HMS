from flask import Blueprint, jsonify, request, current_app, make_response
import json
from flask_security.utils import verify_password, hash_password, login_user, logout_user
import datetime
from flask_restful import Resource, marshal, fields, marshal_with, reqparse

from models import *
from .marshal_fields import user_fields, patient_fields
from services.user_service import UserService

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/auth')

parser = reqparse.RequestParser()
parser.add_argument("user_name", type = str, required = True)
parser.add_argument("user_password", type = str, required = True)
parser.add_argument("email", type = str)
parser.add_argument("contact_number", type = str)

parser.add_argument("patient_id", type = int)
parser.add_argument("name", type = str)
parser.add_argument("dob", type = str)
parser.add_argument("gender", type = str)
parser.add_argument("height", type = str)
parser.add_argument("weight", type = str)

marshal_fields = user_fields
service = UserService

class LoginResource(Resource):
    def post(self):
        args = parser.parse_args()
        user_name = args.get("user_name")
        user_password = args.get("user_password")

        user = User.query.filter(User.user_name == user_name).first()
        if not verify_password(user_password, user.user_password):
            return 400  
        login_user(user)   
        return marshal(user, user_fields), 200

class LogoutResource(Resource):
    def post(self):
        logout_user()

class RegisterResource(Resource):
    def post(self):
        args = parser.parse_args()

        # user table required fields
        user_name = args.get("user_name")
        user_password = args.get("user_password")
        email = args.get("email")
        contact_number = args.get("contact_number")

        # Patient table required fields
        name = args.get('name')
        gender = args.get('gender')
        dob = args.get('dob')
        height = args.get('height')
        weight = args.get('weight')

        datastore = current_app.datastore
        user = User.query.filter(User.user_name == user_name).first()
        print(user)
        
        if user is not None:
            return {'message': 'Already exists'}, 400
                    
        # add as user
        user = datastore.create_user(user_name = user_name, user_password = hash_password(user_password), 
                          contact_number = contact_number, email = email)
        db.session.add(user)
        datastore.add_role_to_user(user, 'Patient')

        # add as patient
        if dob:
            dob = datetime.strptime(dob, '%Y-%m-%d')
        patient = Patient(name = name, gender = gender, dob = dob, 
                                height = height, weight = weight)
        user.user_patient = patient
        db.session.commit()

        #flask-sec login

        return marshal(patient, patient_fields), 201