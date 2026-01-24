from flask import jsonify, request, current_app
from flask_restful import Resource, marshal, reqparse

from models import *
from .marshal_fields import department_fields

class DepartmentResources(Resource):
    def get(self, dept_id):
        dept = Department.query.filter(Department.department_id == dept_id).first()
        if dept:
            return marshal(dept, department_fields)
        return 400
    
class AllDepartmentResources(Resource):
    def get(self):
        all_dept = Department.query.all()
        return marshal(all_dept, department_fields)