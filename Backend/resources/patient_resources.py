from flask import Blueprint, jsonify, request, current_app
from flask_security.utils import verify_password, hash_password
import datetime
from flask_restful import Resource, marshal, reqparse

from models import *
from .marshal_fields import patient_fields

auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/patient')

parser = reqparse.RequestParser()

class PatientResources(Resource):
    def get(self, patient_id):
        patient = Patient.query.filter(Patient.patient_id == patient_id).first()
        if patient:
            return marshal(patient, patient_fields)
        return "Patient not found", 400
    
    def delete(self, patient_id):
        patient = Patient.query.filter(Patient.patient_id == patient_id).first()
        if patient:
            db.session.delete(patient)
            db.session.commit()
            return 200
        return "Patient not found", 400
    
class AllPatientResources(Resource):
    def get(self):
        all_patients = Patient.query.all()
        return marshal(all_patients, patient_fields), 200