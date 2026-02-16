from flask import jsonify, current_app, request
from flask_restful import Resource, marshal, reqparse

from models import *
from .marshal_fields import appointment_fields, slot_fields
from datetime import date

parser = reqparse.RequestParser()
parser.add_argument("date", type = date)

# get the particular 15-15 minutes slots for this particular doctor and selected shift
class SelectShift(Resource):
    def get(self, doctor_id, shift_id):
        shift = Shift.query.filter(Shift.id == shift_id).first()
        all_available_slots = Slots.query.filter(Slots.doctor_id == doctor_id, Slots.shift_id == shift.id).all()
        return marshal(all_available_slots, slot_fields), 200

# book an appointment for a particular patient    
class BookAppointment(Resource):
    def get(self, slot_id):
        slot = Slots.query.filter(Slots.id == slot_id).first()
        return marshal(slot, slot_fields), 200
    
    def patch(self, slot_id):
        slot = Slots.query.filter(Slots.id == slot_id).first()

        # same slot cannot be booked for two patients
        if slot.patient_id != None:
            return "Already booked", 400
        
        data = request.get_json()
        for key in data:
            setattr(slot, key, data[key])

        slot.slots_app = Appointment(date = slot.date, start_time = slot.start_time, end_time = slot.end_time, doctor_id = slot.doctor_id, patient_id = slot.patient_id, status = "Booked")
        db.session.commit()
        return marshal(slot, slot_fields), 200

class AppointmentResources(Resource):
    def get(self, appointment_id):
        appointment = Appointment.query.filter(Appointment.appointment_id == appointment_id).first()
        if appointment:
            return marshal(appointment, appointment_fields)
        return 404
    
class AllAppointmentResources(Resource):
    def get(self):
        all_appointments = Appointment.query.all()
        return marshal(all_appointments, appointment_fields), 200