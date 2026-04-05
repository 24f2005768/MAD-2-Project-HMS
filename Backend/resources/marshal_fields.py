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
    "active": fields.Boolean,
    "user_doctor": fields.Nested({"doctor_id": fields.Integer}),
    "user_patient": fields.Nested({"patient_id": fields.Integer}),
}

doctor_fields = {
    "doctor_id": fields.Integer,
    "name": fields.String,
    "dob": DateField,
    "description": fields.String,
    "gender": fields.String,
    "status": fields.String,
    "pfp": fields.String,
    "doctor_user": fields.Nested({
        'user_name': fields.String,
        'contact_number': fields.String, 
        'email': fields.String,
        'blacklisted': fields.Boolean
        }),
    "dept": fields.Nested({
        "name": fields.String,
        "department_id": fields.Integer
        })
}

department_fields = {
    "department_id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "status": fields.String,
    "doctors": fields.Nested(doctor_fields),
    "pfp": fields.String
}

patient_fields = {
    "patient_id": fields.Integer,
    "name": fields.String,
    "gender": fields.String,
    "dob": DateField,
    "height": fields.String,
    "weight": fields.String,
    "status": fields.String,
    "pfp": fields.String,
    "get_age": fields.String(attribute=lambda patient:patient.get_age()),
    "patient_user": fields.Nested({'user_name': fields.String
                                   ,'contact_number': fields.String, 
                                   'email': fields.String,
                                   'blacklisted': fields.Boolean})
}

treatment_fields = {
    "diagnosis": fields.String,
    "notes": fields.String,
    "prescription": fields.String,
    "tests": fields.String
}

appointment_fields = {
    "appointment_id": fields.Integer,
    "date": DateField,
    "start_time": TimeField,
    "end_time": TimeField,
    "status": fields.String,
    "app_doctor": fields.Nested({'doctor_id': fields.Integer,
                                 'name': fields.String, 
                                 'pfp': fields.String}),
    "app_patient": fields.Nested({'patient_id': fields.Integer,
                                  'name': fields.String, 
                                  'pfp': fields.String}),
    "app_t": fields.Nested(treatment_fields)
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
    "slots_doctor": fields.Nested({"doctor_id": fields.Integer, "name": fields.String}),
    "slots_patient": fields.Nested({"name": fields.String}),
    "slots_shifts": fields.Nested(shift_fields)
}