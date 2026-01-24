from flask import jsonify, current_app, request
from flask_restful import Resource, marshal, reqparse

from models import *
from .marshal_fields import appointment_fields

parser = reqparse.RequestParser()
parser.add_argument("date", type = date)
# parser.add_argument("start_time", type = tim)

class AppointmentResources(Resource):
    def get(self, appointment_id):
        appointment = Appointment.query.filter(Appointment.appointment_id == appointment_id).first()
        if appointment:
            return marshal(appointment, appointment_fields)
        return 400
    
class AllAppointmentResources(Resource):
    def get(self):
        all_appointments = Appointment.query.all()
        return marshal(all_appointments, appointment_fields), 200