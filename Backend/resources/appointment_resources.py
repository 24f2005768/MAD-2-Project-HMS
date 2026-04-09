from flask import jsonify, current_app, request
from flask_restful import Resource, marshal, reqparse
from flask_security import auth_required, roles_required, current_user

from models import *
from caching_config import *
from .marshal_fields import appointment_fields, slot_fields
from datetime import date

# parser for GET requests
get_parser = reqparse.RequestParser()
get_parser.add_argument("all_appointments", type = str, location = "args")

# parser for POST requests
parser = reqparse.RequestParser()

parser.add_argument("diagnosis", type = str)
parser.add_argument("notes", type = str)
parser.add_argument("prescription", type = str)
parser.add_argument("treatment", type = str)

# get the particular 15-15 minutes slots for this particular doctor and selected shift
class SelectShift(Resource):
    def get(self, doctor_id, shift_id):
        # print(shift_id)
        shift = Shift.query.filter(Shift.id == shift_id).first()
        all_available_slots = Slots.query.filter(Slots.doctor_id == doctor_id, Slots.shift_id == shift.id).all()
        
        results = marshal(all_available_slots, slot_fields)

        for i, slot in enumerate(all_available_slots):
            if slot.patient_id is None:
                results[i]["doctor_free"] = True
            else:
                results[i]["doctor_free"] = False

            if current_user.has_role("Patient"):
                slot_shift_id = slot.shift_id
                              
                # If the current patient has already booked an appointment, then show message
                other_bookings = Slots.query.filter(Slots.shift_id == slot_shift_id, Slots.patient_id == current_user.user_patient.patient_id, 
                                                    Slots.id != slot.id, Slots.start_time == slot.start_time).all()
                if other_bookings == []:
                    results[i]["patient_free"] = True
                else:
                    results[i]["patient_free"] = False

        return results, 200

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

        slot.slots_app = Appointment(date = slot.date, start_time = slot.start_time, end_time = slot.end_time, doctor_id = slot.doctor_id, 
                                     patient_id = slot.patient_id, status = "Booked")
        db.session.commit()

        # Clear cache
        invalidate_appointment_caches(doctor_id = slot.doctor_id, patient_id = slot.patient_id)

        return marshal(slot, slot_fields), 200

class AppointmentResources(Resource):
    @auth_required("token")
    @cache.memoize()
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
            doctor_id = appointment.doctor_id
            patient_id = appointment.patient_id

            # this patient's past appointments with this doctor
            past_apt = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.date < date.today(), Appointment.doctor_id == doctor_id, Appointment.appointment_id != appointment.appointment_id).all()
            appointment_data['past_appointment'] = marshal(past_apt, appointment_fields)

            # this patient's upcoming appointments with this doctor
            upcoming_apt = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.date >= date.today(), Appointment.doctor_id == doctor_id, Appointment.appointment_id != appointment.appointment_id).all()
            appointment_data['upcoming_appointment'] = marshal(upcoming_apt, appointment_fields)

            return appointment_data, 200

class AllAppointmentResources(Resource):
    @auth_required("token")
    @cache.memoize()
    def get(self):
        results = {"past_appointments": {}, "upcoming_appointments": {}}

        past_appointments = Appointment.query.filter(Appointment.date < date.today()).all()
        upcoming_appointments = Appointment.query.filter(Appointment.date >= date.today()).all()

        results["past_appointments"] = marshal(past_appointments, appointment_fields)
        results["upcoming_appointments"] = marshal(upcoming_appointments, appointment_fields)
        return results, 200
    
class CancelAppointment(Resource):
    @auth_required("token")
    def patch(self, appointment_id):
        appointment = db.get_or_404(Appointment, appointment_id)

        if current_user.has_role("Doctor"): 
            doctor_id = current_user.user_doctor.doctor_id
            doctor = db.get_or_404(Doctor, doctor_id)
            appointment.status = f"Cancelled by Dr. {doctor.name}"
        
        elif current_user.has_role("Patient"):
            patient_id = current_user.user_patient.patient_id
            patient = db.get_or_404(Patient, patient_id)
            appointment.status = f"Cancelled by {patient.name}"
        else:
            appointment.status = f"Cancelled by Admin"

        # Clear cache for this specific appointment and all appointments list
        invalidate_appointment_caches(appointment_id, appointment.app_doctor.doctor_id, appointment.app_patient.patient_id)
        invalidate_patient_caches(appointment.app_patient.patient_id)
        invalidate_doctor_caches(appointment.app_doctor.doctor_id)

        db.session.commit()
        return marshal(appointment, appointment_fields), 200

class RescheduleAppointment(Resource):
    @auth_required("token")
    def patch(self, appointment_id):
        appointment = db.get_or_404(Appointment, appointment_id)

        # mark appointment as rescheduled
        if current_user.has_role("Patient"):
            patient_id = current_user.user_patient.patient_id
            patient = db.get_or_404(Patient, patient_id)
            appointment.status = f"Rescheduled by {patient.name}"

        elif current_user.has_role("Doctor"):
            doctor_id = current_user.user_doctor.doctor_id
            doctor = db.get_or_404(Doctor, doctor_id)
            appointment.status = f"Rescheduled by Dr. {doctor.name}"

        data = request.get_json()
        new_slot_id = data["slot_id"]
        patient_id = data["patient_id"]
        
        # mark the slot as available for different patients
        old_slot = db.get_or_404(Slots, appointment.slot_id)
        old_slot.patient_id = None

        # book the different slot
        new_slot = db.get_or_404(Slots, new_slot_id)
        new_slot.patient_id = patient_id

        # create new appointment
        appt = Appointment(date = new_slot.date, start_time = new_slot.start_time, end_time = new_slot.end_time, doctor_id = new_slot.doctor_id, 
                            patient_id = patient_id, status = "Booked", slot_id = new_slot.id)
        db.session.add(appt)

        # Clear cache for this specific appointment and all appointments list
        invalidate_appointment_caches(appointment_id, new_slot.doctor_id, patient_id)

        db.session.commit()
        return marshal(appt, appointment_fields), 200

class TreatmentResources(Resource):
    @auth_required("token")
    def post(self, id):
        appointment = db.get_or_404(Appointment, id)
        data = request.get_json()

        diagnosis = data["diagnosis"]
        notes = data["notes"]
        prescription = data["prescription"]
        tests = data["tests"]

        appointment.status = "Completed"

        appointment.app_t = Treatment(diagnosis = diagnosis, notes = notes, prescription = prescription, tests = tests)
        db.session.commit()

        # clear cache
        invalidate_appointment_caches(id, appointment.doctor_id, appointment.patient_id)
        return marshal(appointment, appointment_fields), 201
    
    @auth_required("token")
    def patch(self, id):
        appointment = db.get_or_404(Appointment, id)
        data = request.get_json()
        # print(data)
        diagnosis = data["diagnosis"]
        notes = data["notes"]
        prescription = data["prescription"]
        tests = data["tests"]

        appointment.status = "Completed"

        appointment.app_t = Treatment(diagnosis = diagnosis, notes = notes, prescription = prescription, tests = tests)
        db.session.commit()

        # clear cache
        invalidate_appointment_caches(id, appointment.doctor_id, appointment.patient_id)
        return marshal(appointment, appointment_fields), 200