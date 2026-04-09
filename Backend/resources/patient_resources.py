from flask import request
import datetime
from flask_restful import Resource, marshal, reqparse
from flask_security import auth_required, roles_required, current_user, hash_password

from models import *
from caching_config import *
from .marshal_fields import patient_fields, appointment_fields
from tasks import reminders

# parser for GET requests
get_parser = reqparse.RequestParser()
get_parser.add_argument('past_appointment', type = str, location = 'args')
get_parser.add_argument('upcoming_appointment', type = str, location = 'args')
get_parser.add_argument('today_appointment', type = str, location = 'args')

class PatientResources(Resource):
    @auth_required("token")
    @cache.memoize()
    def get(self, patient_id):
        patient = Patient.query.filter(Patient.patient_id == patient_id).first()
        if not patient:
            return {"message": "Patient does not exist"}, 404
        
        # base data, this will always be sent
        patient_data = marshal(patient, patient_fields)

        # flag to see if appointments of this particular patient are required
        args = get_parser.parse_args()
        flag1 = args.get('upcoming_appointment')
        flag2 = args.get('past_appointment')
        flag3 = args.get('today_appointment')

        # send base data
        if (flag1 == None) and (flag2 == None) and (flag3 == None): 
            return patient_data, 200
        
        # check if the user is a (doctor) or (admin, patient)
        # if user is a doctor only show the Upcoming and Past appointments with this doctor
        if current_user.has_role("Doctor"):
            doctor_id = current_user.user_doctor.doctor_id
            doctor = db.get_or_404(Doctor, doctor_id)

            # this patient's past appointments with this doctor
            past_apt = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.date < date.today(), Appointment.doctor_id == doctor.doctor_id).all()
            patient_data['past_appointment'] = marshal(past_apt, appointment_fields)

            # this patient's upcoming appointments with this doctor
            upcoming_apt = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.date >= date.today(), Appointment.doctor_id == doctor.doctor_id).all()
            patient_data['upcoming_appointment'] = marshal(upcoming_apt, appointment_fields)

        else:
            # this patient's past appointments
            past_apt = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.date < date.today()).all()
            patient_data['past_appointment'] = marshal(past_apt, appointment_fields)

            # this patient's upcoming appointments
            upcoming_apt = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.date > date.today()).all()
            patient_data['upcoming_appointment'] = marshal(upcoming_apt, appointment_fields)
            
            # this patient's today appointments
            today_apt = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.date == date.today()).order_by(Appointment.start_time).all()
            patient_data['today_appointment'] = marshal(today_apt, appointment_fields)

        return patient_data, 200
    
    @auth_required("token")
    @roles_required("Admin")
    def delete(self, patient_id):
        patient = Patient.query.filter(Patient.patient_id == patient_id).first()
        
        # Clear cache for this specific patient and all patients list
        invalidate_patient_caches(patient_id)

        if patient:
            patient_user = patient.patient_user
            db.session.delete(patient_user)

            # delete all slots of patient
            patient_slots = Slots.query.filter(Slots.patient_id == patient_id).all()
            for s in patient_slots:
                db.session.delete(s)

            # delete all appts of doctor
            patient_appts = Appointment.query.filter(Appointment.patient_id == patient_id).all()
            for a in patient_appts:
                db.session.delete(a)

            db.session.delete(patient)
            db.session.commit()
            return 200
        return {"message": "Patient does not exist"}, 404
    
    @auth_required("token")
    def patch(self, patient_id):
        if current_user.has_role('Admin') or (current_user.has_role('Patient') and current_user.user_patient.patient_id == patient_id):
            patient = Patient.query.filter(Patient.patient_id == patient_id).first()
            if not patient:
                return {"message": "Patient does not exist"}, 404
            
            data = request.get_json()
            for key in data:
                # check if DOB is updated
                if key == 'dob' and data[key]:
                    try:
                        dob = datetime.strptime(data[key], '%d-%m-%Y')
                    except:
                        dob = datetime.strptime(data[key], '%Y-%m-%d')
                    setattr(patient, key, dob)
                
                # setting the user table related enteries manually
                elif key in ['user_name', 'contact_number', 'email']:
                        setattr(patient.patient_user, key, data[key])

                elif key == "password":
                    if data[key].strip() != "":
                        patient.patient_user.user_password = hash_password(data[key])

                # check if the patient is blacklisted
                # only admin can blacklist
                elif key == 'blacklist':
                    if current_user.has_role("Admin"):
                        upcoming_apt = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.date >= date.today(), Appointment.status == "Booked").all()
                        if patient.patient_user.blacklisted == False:
                            # blackist this patient
                            patient.patient_user.blacklisted = True
                            # set the active to false so the patient cannot login
                            patient.patient_user.active = False

                            # Cancel all booked upcoming appointments
                            for appt in upcoming_apt:
                                appt.status = "Cancelled by Admin"
                        else:
                            # undo blackist
                            patient.patient_user.blacklisted = False
                            # set the active to true so the patient can login
                            patient.patient_user.active = True
                    else:
                        return {"message": "You are not authorized"}, 403
                    
                else:
                    # for Patient table related values
                    setattr(patient, key, data[key])
            
            # Clear cache for this specific patient and all patients list
            invalidate_patient_caches(patient_id)
            
            db.session.commit()
            return marshal(patient, patient_fields)
        else:
            return {"message": "You are not authorized"}, 403
        
class AllPatientResources(Resource):
    @auth_required("token")
    @cache.memoize()
    def get(self):
        all_patients = Patient.query.all()
        return marshal(all_patients, patient_fields), 200
    
class PatientTreatmentHistory(Resource):
    @auth_required("token")
    @roles_required("Patient")
    def get(self, patient_id):
        result = reminders.treatment_history_patient.delay(patient_id=patient_id)
        return {"message": "Generating report!", "task_id": result.id}, 200