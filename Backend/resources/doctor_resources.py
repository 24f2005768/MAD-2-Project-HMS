from flask import jsonify, request, current_app
from flask_security.utils import verify_password, hash_password
from flask_security import auth_required, roles_required, current_user
from datetime import date, timedelta, time
from flask_restful import Resource, marshal, reqparse
from sqlalchemy import desc

from models import *
from .marshal_fields import doctor_fields, appointment_fields, shift_fields, patient_fields

# parser for GET requests (Doctor)
get_parser = reqparse.RequestParser()
get_parser.add_argument('past_appointment', type = str, location = 'args')
get_parser.add_argument('upcoming_appointment', type = str, location = 'args')
get_parser.add_argument('availability', type = str, location = 'args')
get_parser.add_argument('today_appointment', type = str, location = 'args')
get_parser.add_argument('patients', type = str, location = 'args')

# parser for POST requests
parser = reqparse.RequestParser()

parser.add_argument("user_name", type = str)
parser.add_argument("user_password", type = str)
parser.add_argument("email", type = str)
parser.add_argument("contact_number", type = str)

parser.add_argument("doctor_id", type = int)
parser.add_argument("name", type = str)
parser.add_argument("dob", type = date)
parser.add_argument("description", type = str)
parser.add_argument("gender", type = str)
parser.add_argument("status", type = str)

class DoctorResources(Resource):
    @auth_required("token")
    @roles_required("Admin")
    def post(self):
        args = parser.parse_args()

        # user table required fields
        user_name = args.get("user_name")
        user_password = args.get("user_password")
        email = args.get("email")
        contact_number = args.get("contact_number")

        # doctor table required fields
        name = args.get("name")
        dob = args.get("dob")
        description = args.get("description")
        gender = args.get("gender")

        datastore = current_app.datastore 
        user = datastore.find_user(user_name = user_name)

        if user:
            return {"message": "Doctor already exist"}, 400

        # add as user
        user = datastore.create_user(user_name = user_name, user_password = hash_password(user_password), 
                          contact_number = contact_number, email = email)
        datastore.add_role_to_user(user, 'Doctor')
        db.session.add(user)

        # add as doctor
        doctor = Doctor(name = name, dob = dob, description = description, gender = gender)
        user.user_doctor = doctor

        # add pfp
        m_pfp = db.get_or_404(ProfilePictures, 6)
        f_pfp = db.get_or_404(ProfilePictures, 5)

        
        db.session.commit()

        return marshal(doctor, doctor_fields), 201
    
    @auth_required("token")
    def get(self, doctor_id):
        # Check if user has permission to view this doctor
        # Admins can view any doctor, doctors can only view themselves
        if current_user.has_role('Admin') or (current_user.has_role('Doctor') and current_user.user_doctor.doctor_id == doctor_id):
            doctor = Doctor.query.filter(Doctor.doctor_id == doctor_id).first()
            if not doctor:
                return {"message": "Doctor does not exist"}, 404

            # base data, this will always be sent
            doctor_data = marshal(doctor, doctor_fields)        

            # flag to see if appointments of this particular doctor is required
            args = get_parser.parse_args()
            flag1 = args.get('upcoming_appointment')
            flag2 = args.get('past_appointment')
            flag3 = args.get('availability')
            flag4 = args.get('today_appointment')
            flag5 = args.get('patients')

            # getting all patients of this particular doctor
            # storing the unique patient_id(s) in a set
            d_appointments = doctor.doctor_app 
            p_set = set()   
            for a in d_appointments:
                    p_set.add(a.app_patient.patient_id)
            doctor_data["number_of_patients"] = len(p_set)

            if (flag1 == None) and (flag2 == None) and (flag3 == None) and (flag4 == None) and (flag5 == None): 
                return doctor_data, 200

            # only return base data and patients
            if (flag1 == None) and (flag2 == None) and (flag3 == None) and (flag4 == None) and (flag5):
                # this doctor's patients
                p_dict = {}
                p_list = []

                # getting all patients of this particular doctor
                # storing the unique patient_id(s) in a set

                # fetching and storing the patient objects in a list
                for s in p_set:
                    patient = db.get_or_404(Patient, s)
                    p_list += [patient]
                    # making a dictionary for each patient and storing their appointments
                    p_dict[patient.name] = {}
                    p_dict[patient.name]["patient_data"] = marshal(patient, patient_fields)
                    p_dict[patient.name]["patient_data"]["number_of_appointments"] = 0
                    for a in d_appointments:
                        if a.patient_id == patient.patient_id:
                            p_dict[patient.name]["patient_data"]["number_of_appointments"] += 1
                            p_dict[patient.name][a.appointment_id] = marshal(a, appointment_fields)
                    
                    # storing the last visit of this patient
                    last_visit = Appointment.query.filter(Appointment.doctor_id == doctor.doctor_id, Appointment.patient_id == patient.patient_id).order_by(desc(Appointment.date)).first()
                    p_dict[patient.name]["patient_data"]["last_visit"] = marshal(last_visit, appointment_fields)
                doctor_data['patients'] = p_dict
                return doctor_data, 200

            # doctor availability for the coming dates
            da_list = []
            da = doctor.doctor_shift

            # making a DateTime object
            date_today = date.today()
            time = datetime.min.time()
            date_today = datetime.combine(date_today, time)

            for a in da:
                if a.date >= date_today:
                    da_list += [a]
            doctor_data['availability'] = marshal(da_list, shift_fields)

            # only return base data and availability 
            if (flag1 == None) and (flag2 == None) and (flag3):
                return doctor_data, 200
            
            # today's appointments
            if (flag4):
                today_apt = Appointment.query.filter(Appointment.doctor_id == doctor_id, Appointment.date == date.today()).order_by(Appointment.start_time).all()
                doctor_data['today_appointment'] = marshal(today_apt, appointment_fields)
            
            # flag 2
            # this doctor's past appointments
            past_apt = Appointment.query.filter(Appointment.doctor_id == doctor_id, Appointment.date < date.today()).all()
            doctor_data['past_appointment'] = marshal(past_apt, appointment_fields)
            
            # flag 1
            # this doctor's upcoming appointments
            upcoming_apt = Appointment.query.filter(Appointment.doctor_id == doctor_id, Appointment.date > date.today()).all()
            doctor_data['upcoming_appointment'] = marshal(upcoming_apt, appointment_fields)

            return doctor_data, 200
        else: 
            return {"message": "You are not authorized"}, 403
        
    @auth_required("token")
    @roles_required("Admin")
    def delete(self, doctor_id):
        doctor = Doctor.query.filter(Doctor.doctor_id == doctor_id).first()
        if doctor:
            db.session.delete(doctor)
            db.session.commit()
            return 200
        return {"message": "Doctor does not exist"}, 404
    
    @auth_required("token")
    def patch(self, doctor_id):
        if current_user.has_role('Admin') or (current_user.has_role('Doctor') and current_user.user_doctor.doctor_id == doctor_id):
            doctor = Doctor.query.filter(Doctor.doctor_id == doctor_id).first()
            if not doctor:
                return {"message": "Doctor does not exist"}, 404

            data = request.get_json()
            print(data.keys())
            for key in data:
                # check if DOB is updated
                if key == 'dob' and data[key]:
                    try:
                        dob = datetime.strptime(data[key], '%d-%m-%Y')
                    except:
                        dob = datetime.strptime(data[key], '%Y-%m-%d')
                    setattr(doctor, key, dob)
                
                # setting the user table related enteries manually
                elif key == "user_name":
                    doctor.doctor_user.user_name = data[key]

                elif key == "contact_number":
                    doctor.doctor_user.contact_number = data[key]

                elif key == "email":
                    doctor.doctor_user.email = data[key]

                elif key == "password":
                    doctor.doctor_user.user_password = hash_password(data[key])

                # check if the doctor is blacklisted
                # only doctor can blacklist
                elif key == 'blacklist':
                    if current_user.has_role("Admin"):
                        if doctor.doctor_user.blacklisted == False:
                            # blackist this doctor
                            doctor.doctor_user.blacklisted = True
                            # set the active to false so the doctor cannot login
                            doctor.doctor_user.active = False

                        else:
                            # undo blackist
                            doctor.doctor_user.blacklisted = False
                            # set the active to true so the doctor can login
                            doctor.doctor_user.active = True
                    else:
                        return {"message": "You are not authorized"}, 403
                    
                else:
                    setattr(doctor, key, data[key])
            db.session.commit()
            return marshal(doctor, doctor_fields)
        else:
            return {"message": "You are not authorized"}, 403
        
class AllDoctorResources(Resource):
    @auth_required("token")
    def get(self):
        args = get_parser.parse_args()
        flag = args.get('limit')
        if flag == None:
            all_doctors = Doctor.query.all()
        return marshal(all_doctors, doctor_fields), 200
    
class Availability(Resource):
    @auth_required("token")
    def get(self, doctor_id):
        doctor = db.get_or_404(Doctor, doctor_id)
        doctor_shift = doctor.doctor_shift

        all_shifts = Shift.query.all()
        next_week_dates = [(date.today() + timedelta(days = i)) for i in range(1,8)]

        shifts = {}
        for d in next_week_dates:
            # keys should be strings, so we convert the dates to strings
            d_str = datetime.strftime(d, '%d-%m-%Y')
            shifts[d_str] = []

        for d in shifts:
            for s in all_shifts:
                # convert back into datetime object to compare
                d_dt = datetime.strptime(d, '%d-%m-%Y')

                # find if doctor has already given availability for this week or not
                if s.date == d_dt:
                    if s in doctor_shift:
                        d_str = datetime.strftime(d_dt, '%d-%m-%Y')
                        s_marshaled = marshal(s, shift_fields)
                        # adding if the doctor is available for this shift
                        # when updating availability, if updated_availability changes then update availability
                        # we are not working on original_availability, it is only for checking differences if the availability is updated
                        s_marshaled["original_availability"] = 1
                        s_marshaled["updated_availability"] = 1
                        shifts[d_str] += [s_marshaled]
                    else:
                        d_str = datetime.strftime(d_dt, '%d-%m-%Y')
                        s_marshaled = marshal(s, shift_fields)
                        # adding if the doctor is not available for this shift
                        s_marshaled["original_availability"] = 0
                        s_marshaled["updated_availability"] = 0
                        shifts[d_str] += [s_marshaled]
        return shifts, 200
    
    @auth_required("token")
    def patch(self, doctor_id):
        doctor = db.get_or_404(Doctor, doctor_id)

        data = request.get_json()
        for key in data:
            for d in data[key]:
                if d["original_availability"] != d["updated_availability"]:

                    # add any new available slots and break them into 15 minutes time
                    if (d["original_availability"] == 0) and (d["updated_availability"] == 1):
                        d_dt = datetime.strptime(d["date"], "%d-%m-%Y")
                        shift = Shift.query.filter(Shift.date == d_dt, Shift.name == d["name"]).first()

                        # ensure that we are not repeatedly adding shifts
                        if shift and shift not in doctor.doctor_shift:
                            doctor.doctor_shift.append(shift)

                            start_time = shift.start_time
                            end_time = shift.end_time

                            while start_time != end_time:
                                new_time = timedelta(minutes = 15) + start_time
                                new_slot = Slots(date = shift.date, start_time = start_time, end_time = new_time, doctor_id = doctor.doctor_id, shift_id = shift.id)
                                db.session.add(new_slot)
                                start_time = new_time 

                    if (d["original_availability"] == 1) and (d["updated_availability"] == 0):
                        d_dt = datetime.strptime(d["date"], "%d-%m-%Y")
                        shift = Shift.query.filter(Shift.date == d_dt, Shift.name == d["name"]).first()
                        all_slots = Slots.query.filter(Slots.shift_id == shift.id).all()
                        for slot in all_slots:
                            # mark any appointments as cancelled
                            db.session.delete(slot)
                        
                        # remove from database
                        doctor.doctor_shift.remove(shift)
            db.session.commit()

class DoctorAppointments(Resource):
    @auth_required("token")
    def get(self, doctor_id):
        # Check if user has permission to view this doctor
        # Admins can view any doctor, doctors can only view themselves
        if current_user.has_role('Admin') or (current_user.has_role('Doctor') and current_user.user_doctor.doctor_id == doctor_id):
            doctor = db.get_or_404(Doctor, doctor_id)
            if not doctor:
                return {"message": "Doctor does not exist"}, 404
            
            appointments = {"today": {}, "this_week": {}, "past": {}}

            today_appt = Appointment.query.filter(Appointment.date == date.today(), Appointment.doctor_id == doctor.doctor_id).order_by(Appointment.start_time).all()
            this_week_appt = Appointment.query.filter(Appointment.date > date.today(), Appointment.doctor_id == doctor.doctor_id).order_by(Appointment.date, Appointment.start_time).all()
            past_appt = Appointment.query.filter(Appointment.date < date.today(), Appointment.doctor_id == doctor.doctor_id).order_by(desc(Appointment.date), Appointment.start_time).all()

            appointments["today"] = marshal(today_appt, appointment_fields)
            appointments["this_week"] = marshal(this_week_appt, appointment_fields)
            appointments["past"] = marshal(past_appt, appointment_fields)

            return appointments, 200
        else:
            return {"message": "You are not authorized"}, 403
