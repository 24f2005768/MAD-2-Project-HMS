from flask import jsonify, request, current_app
from flask_security.utils import verify_password, hash_password, login_user, logout_user
import datetime
from flask_restful import Resource, marshal, reqparse
from flask_security import auth_required, roles_required, current_user

from models import *
from caching_config import *
from .marshal_fields import user_fields, patient_fields

# Parser for login
login_parser = reqparse.RequestParser()
login_parser.add_argument("user_name", type = str, required = True)
login_parser.add_argument("user_password", type = str, required = True)

# Parser for registering as a patient
parser = reqparse.RequestParser()
parser.add_argument("user_name", type = str, required = True)
parser.add_argument("user_password", type = str, required = True)
parser.add_argument("email", type = str, required = True)
parser.add_argument("contact_number", type = str)

parser.add_argument("patient_id", type = int)
parser.add_argument("name", type = str, required = True)
parser.add_argument("dob", type = str)
parser.add_argument("gender", type = str)
parser.add_argument("height", type = str)
parser.add_argument("weight", type = str)

class LoginResource(Resource):
    def post(self):
        args = login_parser.parse_args()
        user_name = args.get("user_name")
        user_password = args.get("user_password")

        user = User.query.filter(User.user_name == user_name).first()
        if user == None:
            return {"message": "User does not exist"}, 404
        
        if not verify_password(user_password, user.user_password):
            return {"message": "Invalid Username or Password"}, 404
        login_user(user)   

        response_data = marshal(user, user_fields)
        
        # Add role-specific IDs
        if user.role() == 'Doctor' and user.user_doctor:
            response_data["doctor_id"] = user.user_doctor.doctor_id

        elif user.role() == 'Patient' and user.user_patient:
            response_data["patient_id"] = user.user_patient.patient_id
            
        return response_data, 200

class LogoutResource(Resource):
    @auth_required("token")
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
        
        if user is not None:
            return {'message': 'User Already exists'}, 400
                    
        # add as user
        if (user_name != "" and user_password != "" and email != ""):
            user = datastore.create_user(user_name = user_name, user_password = hash_password(user_password), 
                            contact_number = contact_number, email = email)
            db.session.add(user)
            datastore.add_role_to_user(user, 'Patient')
        else:
            return {"message": "User name, password and email are required"}, 400

        # add as patient
        if dob:
            dob = datetime.strptime(dob, '%Y-%m-%d')
        if (name != ""):
            patient = Patient(name = name, gender = gender, dob = dob, 
                                    height = height, weight = weight)
            user.user_patient = patient
            db.session.commit()

            # clear cache 
            invalidate_patient_caches()
            return marshal(patient, patient_fields), 201
        else:
            return {"message": "Name is required"}, 400   