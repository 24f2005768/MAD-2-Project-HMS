from flask import request
from flask_restful import Resource, marshal, reqparse
from sqlalchemy import or_
from flask_security import auth_required, roles_required, current_user

from models import *
from .marshal_fields import *

# parser for GET requests
get_parser = reqparse.RequestParser()
get_parser.add_argument("query", type = str, location = "args")

class AdminSearch(Resource):
    @auth_required("token")
    @roles_required("Admin")
    def get(self):
        args = get_parser.parse_args()
        search_query = args.get("query")

        results = {"patients": {"ID":{}, "name": {}, "contact_number": {}, "email": {}}, 
                   "doctors": {"ID":{}, "name": {}, "contact_number": {}, "email": {}},
                    "departments": {"ID":{}, "name": {}}}

        # filter out patients by {ID, name, CN, email}
        patient_by_ID = Patient.query.join(User).filter(Patient.patient_id.like(f"%{search_query}%")).all()
        results["patients"]["ID"] = marshal(patient_by_ID, patient_fields)

        patient_by_name = Patient.query.join(User).filter(Patient.name.like(f"%{search_query}%")).all()
        results["patients"]["name"] = marshal(patient_by_name, patient_fields)

        patient_by_contact_number = Patient.query.join(User).filter(User.contact_number.like(f"%{search_query}%")).all()
        results["patients"]["contact_number"] = marshal(patient_by_contact_number, patient_fields)

        patient_by_email = Patient.query.join(User).filter(User.email.like(f"%{search_query}%")).all()
        results["patients"]["email"] = marshal(patient_by_email, patient_fields)

        # filter out doctors by {ID, name, CN, email}
        doctor_by_ID = Doctor.query.join(User).filter(Doctor.doctor_id.like(f"%{search_query}%")).all()
        results["doctors"]["ID"] = marshal(doctor_by_ID, doctor_fields)

        doctor_by_name = Doctor.query.join(User).filter(Doctor.name.like(f"%{search_query}%")).all()
        results["doctors"]["name"] = marshal(doctor_by_name, doctor_fields)

        doctor_by_contact_number = Doctor.query.join(User).filter(User.contact_number.like(f"%{search_query}%")).all()
        results["doctors"]["contact_number"] = marshal(doctor_by_contact_number, doctor_fields)

        doctor_by_email = Doctor.query.join(User).filter(User.email.like(f"%{search_query}%")).all()
        results["doctors"]["email"] = marshal(doctor_by_email, doctor_fields)

        # filter out departments by (ID, name)
        dept_by_ID = Department.query.filter(Department.department_id.like(f"%{search_query}%")).all()
        results["departments"]["ID"] = marshal(dept_by_ID, department_fields)

        dept_by_name = Department.query.filter(Department.name.like(f"%{search_query}%")).all()
        results["departments"]["name"] = marshal(dept_by_name, department_fields)
        
        return results, 200