from flask import request
from flask_restful import Resource, marshal, reqparse
from sqlalchemy import or_, desc
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
    
class DoctorSearch(Resource):
    @auth_required("token")
    @roles_required("Doctor")
    def get(self):
        args = get_parser.parse_args()
        search_query = args.get("query")

        doctor = db.get_or_404(Doctor, current_user.user_doctor.doctor_id)
        results = {"patients": {"name": [], "contact_number": [], "email": []}, 
                   "doctors": {"name": {}, "contact_number": {}, "email": {}},
                    "departments": {"name": {}}}

        # get the patients of this doctor
        d_appointments = doctor.doctor_app 
        p_set = set()   
        for a in d_appointments:
                p_set.add(a.app_patient.patient_id)

        p_dict = {}
        p_list = []

        # getting all patients of this particular doctor
        # storing the unique patient_id(s) in a set

        # fetching and storing the patient objects in a list
        for s in p_set:
            patient = db.get_or_404(Patient, s)
            p_list += [patient]
            # making a dictionary for each patient and storing their appointments
            p_dict[patient.name] = {}
            p_dict[patient.name]["patient_data"] = marshal(patient, patient_fields)
            p_dict[patient.name]["patient_data"]["number_of_appointments"] = 0
            for a in d_appointments:
                if a.patient_id == patient.patient_id:
                    p_dict[patient.name]["patient_data"]["number_of_appointments"] += 1
                    p_dict[patient.name][a.appointment_id] = marshal(a, appointment_fields)
            
            # storing the last visit of this patient
            last_visit = Appointment.query.filter(Appointment.doctor_id == doctor.doctor_id, Appointment.patient_id == patient.patient_id, Appointment.date <= date.today()).order_by(desc(Appointment.date)).first()
            if last_visit == None:
                p_dict[patient.name]["patient_data"]["last_visit"] = {}    
            else:
                p_dict[patient.name]["patient_data"]["last_visit"] = marshal(last_visit, appointment_fields)

        # filter out patients by {name, CN, email}        
        patient_by_name = Patient.query.join(User).filter(Patient.name.like(f"%{search_query}%")).all()
        for i in patient_by_name:
            if i in p_list:
                patient = marshal(i, patient_fields)
                patient["number_of_appointments"] = p_dict[i.name]["patient_data"]["number_of_appointments"]
                patient["last_visit"] = p_dict[i.name]["patient_data"]["last_visit"]
                results["patients"]["name"].append(patient)

        patient_by_contact_number = Patient.query.join(User).filter(User.contact_number.like(f"%{search_query}%")).all()
        for i in patient_by_contact_number:
            if i in p_list:
                patient = marshal(i, patient_fields)
                patient["number_of_appointments"] = p_dict[i.name]["patient_data"]["number_of_appointments"]
                patient["last_visit"] = p_dict[i.name]["patient_data"]["last_visit"]
                results["patients"]["contact_number"].append(patient)

        patient_by_email = Patient.query.join(User).filter(User.email.like(f"%{search_query}%")).all()
        for i in patient_by_email:
            if i in p_list:
                patient = marshal(i, patient_fields)
                patient["number_of_appointments"] = p_dict[i.name]["patient_data"]["number_of_appointments"]
                patient["last_visit"] = p_dict[i.name]["patient_data"]["last_visit"]
                results["patients"]["email"].append(patient)

        # filter out doctors by {name, CN, email}
        doctor_by_name = Doctor.query.join(User).filter(Doctor.name.like(f"%{search_query}%")).all()
        results["doctors"]["name"] = marshal(doctor_by_name, doctor_fields)

        doctor_by_contact_number = Doctor.query.join(User).filter(User.contact_number.like(f"%{search_query}%")).all()
        results["doctors"]["contact_number"] = marshal(doctor_by_contact_number, doctor_fields)

        doctor_by_email = Doctor.query.join(User).filter(User.email.like(f"%{search_query}%")).all()
        results["doctors"]["email"] = marshal(doctor_by_email, doctor_fields)

        # filter out departments by (name)
        dept_by_name = Department.query.filter(Department.name.like(f"%{search_query}%")).all()
        results["departments"]["name"] = marshal(dept_by_name, department_fields)

        return results, 200
    
class PatientSearch(Resource):
    @auth_required("token")
    @roles_required("Patient")
    def get(self):
        args = get_parser.parse_args()
        search_query = args.get("query")

        results = {"doctors": {"name": {}, "contact_number": {}, "email": {}},
                    "departments": {"name": {}}}
        
        # filter out doctors by {name, CN, email}
        doctor_by_name = Doctor.query.join(User).filter(Doctor.name.like(f"%{search_query}%")).all()
        results["doctors"]["name"] = marshal(doctor_by_name, doctor_fields)

        doctor_by_contact_number = Doctor.query.join(User).filter(User.contact_number.like(f"%{search_query}%")).all()
        results["doctors"]["contact_number"] = marshal(doctor_by_contact_number, doctor_fields)

        doctor_by_email = Doctor.query.join(User).filter(User.email.like(f"%{search_query}%")).all()
        results["doctors"]["email"] = marshal(doctor_by_email, doctor_fields)

        # filter out departments by (name)
        dept_by_name = Department.query.filter(Department.name.like(f"%{search_query}%")).all()
        results["departments"]["name"] = marshal(dept_by_name, department_fields)

        return results, 200
