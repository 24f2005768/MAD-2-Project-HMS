from flask import request
import datetime
from flask_restful import Resource, marshal, reqparse

from models import *
from .marshal_fields import patient_fields, appointment_fields

# parser for GET requests
get_parser = reqparse.RequestParser()
get_parser.add_argument('past_appointment', type = str, location = 'args')
get_parser.add_argument('upcoming_appointment', type = str, location = 'args')

class PatientResources(Resource):
    def get(self, patient_id):
        patient = Patient.query.filter(Patient.patient_id == patient_id).first()
        if not patient:
            return 'Patient not found', 404
        
        # base data, this will always be sent
        patient_data = marshal(patient, patient_fields)

        # flag to see if appointments of this particular patient are required
        args = get_parser.parse_args()
        flag1 = args.get('upcoming_appointment')
        flag2 = args.get('past_appointment')

        # send base data
        if (flag1 == None) and (flag2 == None): 
            return patient_data, 200
        
        # this patient's past appointments
        past_apt = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.date < date.today()).all()
        patient_data['past_appointment'] = marshal(past_apt, appointment_fields)

        # this patient's upcoming appointments
        upcoming_apt = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.date >= date.today()).all()
        patient_data['upcoming_appointment'] = marshal(upcoming_apt, appointment_fields)

        return patient_data, 200
    
    def delete(self, patient_id):
        patient = Patient.query.filter(Patient.patient_id == patient_id).first()
        if patient:
            db.session.delete(patient)
            db.session.commit()
            return 200
        return "Patient not found", 404
    
    def patch(self, patient_id):
        patient = Patient.query.filter(Patient.patient_id == patient_id).first()
        if not patient:
            return 'Patient not found', 404
        
        data = request.get_json()
        for key in data:
            if key == 'dob' and data[key]:
                try:
                    dob = datetime.strptime(data[key], '%d-%m-%Y')
                except:
                    dob = datetime.strptime(data[key], '%Y-%m-%d')
                setattr(patient, key, dob)
            else:
                setattr(patient, key, data[key])
        db.session.commit()
        return marshal(patient, patient_fields)
    
class AllPatientResources(Resource):
    def get(self):
        all_patients = Patient.query.all()
        return marshal(all_patients, patient_fields), 200