from flask_restful import Resource, marshal, reqparse
from flask import request
from datetime import date
from flask_security import auth_required, roles_required, current_user

from models import *
from caching_config import *
from .marshal_fields import department_fields, appointment_fields

# parser for GET requests
get_parser = reqparse.RequestParser()
get_parser.add_argument('past_appointment', type = str, location = 'args')
get_parser.add_argument('upcoming_appointment', type = str, location = 'args')

# parser for POST requests
parser = reqparse.RequestParser()
parser.add_argument("name", type = str, required = True)
parser.add_argument("description", type = str)

class DepartmentResources(Resource):
    @auth_required("token")
    @roles_required("Admin")
    def post(self):
        args = parser.parse_args()
        dept_name = args.get('name')
        description = args.get("description")

        dept = Department.query.filter(Department.name == dept_name).first()
        if dept:
            return {"message": "Department already exists"}, 404
        if description == "":
            description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum"
        dept = Department(name = dept_name, description = description)
        db.session.add(dept)
        db.session.commit()

        # Clear cache for all departments
        invalidate_department_caches()

        return marshal(dept, department_fields), 200
    
    @auth_required("token")
    @cache.memoize()
    def get(self, dept_id):
        print(f"Caching department {dept_id} for user {current_user.user_id}")
        dept = Department.query.filter(Department.department_id == dept_id).first()
        if not dept:
            return {"message": "Department does not exist"}, 404
        
        # base data, this will always be sent
        dept_data = marshal(dept, department_fields)

        # flag to see if appointments of this particular dept is required
        args = get_parser.parse_args()
        flag1 = args.get('upcoming_appointment')
        flag2 = args.get('past_appointment')
        
        # only return base data
        if (flag1 == None) and (flag2 == None):
            return dept_data, 200
        
        dept_data["past_appointment"] = []
        dept_data["upcoming_appointment"] = []

        for doctor in dept.doctors:
            # this doctor's past appointments
            if current_user.has_role("Patient"):
                patient = db.get_or_404(Patient, current_user.user_patient.patient_id)
                past_apt = Appointment.query.filter(Appointment.doctor_id == doctor.doctor_id, Appointment.patient_id == patient.patient_id, Appointment.date < date.today()).all()
            else:
                past_apt = Appointment.query.filter(Appointment.doctor_id == doctor.doctor_id, Appointment.date < date.today()).all()
            dept_data['past_appointment'] += marshal(past_apt, appointment_fields)

            # this doctor's upcoming appointments
            if current_user.has_role("Patient"):
                patient = db.get_or_404(Patient, current_user.user_patient.patient_id)
                upcoming_apt = Appointment.query.filter(Appointment.doctor_id == doctor.doctor_id, Appointment.patient_id == patient.patient_id,  Appointment.date >= date.today()).all()
            else:
                upcoming_apt = Appointment.query.filter(Appointment.doctor_id == doctor.doctor_id, Appointment.date >= date.today()).all()
            dept_data['upcoming_appointment'] += marshal(upcoming_apt, appointment_fields)

        return dept_data, 200
    
    @auth_required("token")
    @roles_required("Admin")
    def delete(self, dept_id):
        dept = Department.query.filter(Department.department_id == dept_id).first()

        if dept:
            for doctor in dept.doctors:

                # delete doctor as user
                doctor_user = doctor.doctor_user
                db.session.delete(doctor_user)

                # delete all slots of doctor
                doctor_slots = Slots.query.filter(Slots.doctor_id == doctor.doctor_id).all()
                for s in doctor_slots:
                    db.session.delete(s)

                # delete all appts of doctor
                doctor_appts = Appointment.query.filter(Appointment.doctor_id == doctor.doctor_id).all()
                for a in doctor_appts:
                    db.session.delete(a)

                # delete doctor
                db.session.delete(doctor)
            
            db.session.delete(dept)
            db.session.commit()

            # Clear cache for this specific department and all departments list
            invalidate_department_caches(dept_id)
                      
            return {"message": "Department deleted successfully"}, 200
        return {"message": "Department does not exist"}, 404
    
    @auth_required("token")
    @roles_required("Admin")
    def patch(self, dept_id):
        dept = Department.query.filter(Department.department_id == dept_id).first()
        if not dept:
            return {"message": "Department does not exist"}, 404
        
        data = request.get_json()
        for key in data:
            setattr(dept, key, data[key])
        db.session.commit() 

        # Clear cache for this department and all departments list
        invalidate_department_caches(dept_id)

        return marshal(dept, department_fields), 200      

class AllDepartmentResources(Resource):
    @auth_required("token")
    @cache.memoize()
    def get(self):
        all_dept = Department.query.all()
        return marshal(all_dept, department_fields)