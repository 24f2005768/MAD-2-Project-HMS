from flask_restful import Resource, marshal, reqparse
from flask import request

from models import *
from .marshal_fields import department_fields

parser = reqparse.RequestParser()
parser.add_argument("name", type = str, required = True)
parser.add_argument("description", type = str)

class DepartmentResources(Resource):
    def get(self, dept_id):
        dept = Department.query.filter(Department.department_id == dept_id).first()
        if dept:
            return marshal(dept, department_fields)
        return 400
    
    def post(self):
        args = parser.parse_args()
        dept_name = args.get('name')
        description = args.get("description")

        dept = Department.query.filter(Department.name == dept_name).first()
        if dept:
            return 'Already exists', 400
        dept = Department(name = dept_name, description = description)
        db.session.add(dept)
        db.session.commit()
        return marshal(dept, department_fields), 200
    
    def patch(self, dept_id):
        dept = Department.query.filter(Department.department_id == dept_id).first()
        if not dept:
            return 'Not found', 400
        
        data = request.get_json()
        for key in data:
            setattr(dept, key, data[key])
        db.session.commit()  
        return marshal(dept, department_fields), 200      

class AllDepartmentResources(Resource):
    def get(self):
        all_dept = Department.query.all()
        return marshal(all_dept, department_fields)