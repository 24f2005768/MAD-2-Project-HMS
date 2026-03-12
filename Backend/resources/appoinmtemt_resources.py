from flask import jsonify, current_app, request
from flask_restful import Resource, marshal, reqparse
from flask_security import auth_required, roles_required, current_user

from models import *
from .marshal_fields import appointment_fields, slot_fields
from datetime import date

# parser for GET requests
get_parser = reqparse.RequestParser()
get_parser.add_argument("all_appointments", type = str, location = "args")

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
    @auth_required("token")
    def get(self, slot_id):
        slot = Slots.query.filter(Slots.id == slot_id).first()
        return marshal(slot, slot_fields), 200
    
    @auth_required("token")
    def patch(self, slot_id):
        slot = Slots.query.filter(Slots.id == slot_id).first()

        # same slot cannot be booked for two patients
        if slot.patient_id != None:
            return {"message": "This slot is already booked"}, 400
        
        data = request.get_json()
        for key in data:
            setattr(slot, key, data[key])

        slot.slots_app = Appointment(date = slot.date, start_time = slot.start_time, end_time = slot.end_time, doctor_id = slot.doctor_id, patient_id = slot.patient_id, status = "Booked")
        db.session.commit()
        return marshal(slot, slot_fields), 200

class AppointmentResources(Resource):
    # @auth_required("token")
    def get(self, appointment_id):
        # base data
        appointment_data = {}

        # flag to see if other appointments are required
        args = get_parser.parse_args()
        flag = args.get("all_appointments")

        appointment = Appointment.query.filter(Appointment.appointment_id == appointment_id).first()
        if appointment:
            appointment_data = marshal(appointment, appointment_fields)
        else:
            return {"message": "Appointment does not exist"}, 404
        
        if (flag == None):
            return appointment_data, 200
        else:
            if current_user.has_role("Doctor"):
                doctor_id = current_user.user_doctor.doctor_id
                patient_id = appointment.patient_id
                doctor = db.get_or_404(Doctor, doctor_id)

                # this patient's past appointments with this doctor
                past_apt = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.date < date.today(), Appointment.doctor_id == doctor.doctor_id, Appointment.appointment_id != appointment.appointment_id).all()
                appointment_data['past_appointment'] = marshal(past_apt, appointment_fields)

                # this patient's upcoming appointments with this doctor
                upcoming_apt = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.date >= date.today(), Appointment.doctor_id == doctor.doctor_id, Appointment.appointment_id != appointment.appointment_id).all()
                appointment_data['upcoming_appointment'] = marshal(upcoming_apt, appointment_fields)

                return appointment_data


class AllAppointmentResources(Resource):
    @auth_required("token")
    def get(self):
        all_appointments = Appointment.query.all()
        return marshal(all_appointments, appointment_fields), 200
    
class CancelAppointment(Resource):
    @auth_required("token")
    def patch(self, appointment_id):
        appointment = db.get_or_404(Appointment, appointment_id)
        if current_user.has_role("Doctor"): 
            doctor_id = current_user.user_doctor.doctor_id
            doctor = db.get_or_404(Doctor, doctor_id)
            appointment.status = f"Cancelled by Dr. {doctor.name}"
        db.session.commit()