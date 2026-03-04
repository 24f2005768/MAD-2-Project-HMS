from flask_restful import Resource, marshal, reqparse
from flask import request
from datetime import date
from flask_security import auth_required, roles_required, current_user

from models import *
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
            return {"message": "Department does not exist"}, 404
        dept = Department(name = dept_name, description = description)
        db.session.add(dept)
        db.session.commit()
        return marshal(dept, department_fields), 200
    
    @auth_required("token")
    def get(self, dept_id):
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
            past_apt = Appointment.query.filter(Appointment.doctor_id == doctor.doctor_id, Appointment.date < date.today()).all()
            dept_data['past_appointment'] += marshal(past_apt, appointment_fields)

            # this doctor's upcoming appointments
            upcoming_apt = Appointment.query.filter(Appointment.doctor_id == doctor.doctor_id, Appointment.date >= date.today()).all()
            dept_data['upcoming_appointment'] += marshal(upcoming_apt, appointment_fields)

        return dept_data, 200
    
    @auth_required("token")
    @roles_required("Admin")
    def delete(self, dept_id):
        dept = Department.query.filter(Department.department_id == dept_id).first()
        if dept:
            db.session.delete(dept)
            db.session.commit()
            return 200
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
        return marshal(dept, department_fields), 200      

class AllDepartmentResources(Resource):
    @auth_required("token")
    def get(self):
        all_dept = Department.query.all()
        return marshal(all_dept, department_fields)