from flask import Blueprint, jsonify, request, current_app
from flask_security.utils import verify_password, hash_password
import datetime
from flask_restful import Resource, marshal, reqparse

from models import *
from .marshal_fields import doctor_fields

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/doctor')

parser = reqparse.RequestParser()
parser.add_argument("user_name", type = str)
parser.add_argument("user_password", type = str)
parser.add_argument("email", type = str)
parser.add_argument("contact_number", type = str)

parser.add_argument("doctor_id", type = int)
parser.add_argument("name", type = str)
parser.add_argument("dob", type = date)
parser.add_argument("description", type = str)
parser.add_argument("gender", type = str)
parser.add_argument("status", type = str)

class DoctorResources(Resource):
    def post(self):
        args = parser.parse_args()

        # user table required fields
        user_name = args.get("user_name")
        user_password = args.get("user_password")
        email = args.get("email")
        contact_number = args.get("contact_number")

        # doctor table required fields
        name = args.get("name")
        dob = args.get("dob")
        description = args.get("description")
        gender = args.get("gender")

        datastore = current_app.datastore 
        user = datastore.find_user(user_name = user_name)

        if user:
            return jsonify({'message': 'Already exists'}), 400

        # add as user
        user = datastore.create_user(user_name = user_name, user_password = hash_password(user_password), 
                          contact_number = contact_number, email = email)
        datastore.add_role_to_user(user, 'Doctor')
        db.session.add(user)

        # add as doctor
        doctor = Doctor(name = name, dob = dob, description = description, gender = gender)
        user.user_doctor = doctor
        db.session.commit()

        return marshal(doctor, doctor_fields), 201
    
    def get(self, doctor_id):
        doctor = Doctor.query.filter(Doctor.doctor_id == doctor_id).first()
        if doctor:
            return marshal(doctor, doctor_fields), 200
        else:
            400

    def delete(self, doctor_id):
        doctor = Doctor.query.filter(Doctor.doctor_id == doctor_id).first()
        if doctor:
            db.session.delete(doctor)
            db.session.commit()
            return 200
        return 400
    
class AllDoctorResources(Resource):
    def get(self):
        all_doctors = Doctor.query.all()
        return marshal(all_doctors, doctor_fields), 200