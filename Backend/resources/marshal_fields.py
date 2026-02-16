from flask_restful import fields
from datetime import datetime

class DateField(fields.Raw):
    def format(self, value):
        return datetime.strftime(value, '%d-%m-%Y')

class TimeField(fields.Raw):
    def format(self, value):        
        return datetime.strftime(value, '%H:%M')

admin_fields = {
    "name": fields.String
}

user_fields = {
    "user_id": fields.Integer,
    "user_name": fields.String,
    "contact_number": fields.String,
    "email": fields.String,
    "role": fields.String(attribute=lambda user:user.role()),
    "token": fields.String(attribute=lambda user:user.get_auth_token()),
    "blacklisted": fields.Boolean,
    "active": fields.Boolean
}

department_fields = {
    "department_id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "status": fields.String,
    "doctors": fields.Nested({'name': fields.String, "description": fields.String})
}

doctor_fields = {
    "doctor_id": fields.Integer,
    "name": fields.String,
    "dob": DateField,
    "description": fields.String,
    "gender": fields.String,
    "status": fields.String,
    "doctor_user": fields.Nested({
        'contact_number': fields.String, 
        'email': fields.String,
        'blacklisted': fields.Boolean})
}

patient_fields = {
    "patient_id": fields.Integer,
    "name": fields.String,
    "gender": fields.String,
    "dob": DateField,
    "height": fields.String,
    "weight": fields.String,
    "status": fields.String,
    "patient_user": fields.Nested({'contact_number': fields.String, 'email': fields.String})
}

appointment_fields = {
    "appointment_id": fields.Integer,
    "date": DateField,
    "start_time": TimeField,
    "end_time": TimeField,
    "status": fields.String,
    "app_doctor": fields.Nested({'name': fields.String}),
    "app_patient": fields.Nested({'name': fields.String})
}

shift_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "date": DateField,
    "start_time": TimeField,
    "end_time": TimeField
}

slot_fields = {
    "id": fields.Integer,
    "date": DateField,
    "start_time": TimeField,
    "end_time": TimeField,
    "slots_doctor": fields.Nested({"name": fields.String}),
    "slots_patient": fields.Nested({"name": fields.String}),
}