from flask import jsonify, request, current_app
from flask_security.utils import verify_password, hash_password
from datetime import date
from flask_restful import Resource, marshal, reqparse

from models import *
from .marshal_fields import doctor_fields, appointment_fields, shift_fields

# parser for GET requests
get_parser = reqparse.RequestParser()
get_parser.add_argument('past_appointment', type = str, location = 'args')
get_parser.add_argument('upcoming_appointment', type = str, location = 'args')
get_parser.add_argument('availability', type = str, location = 'args')

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
            return jsonify({'message': 'Already exists'}), 404

        # add as user
        user = datastore.create_user(user_name = user_name, user_password = hash_password(user_password), 
                          contact_number = contact_number, email = email)
        datastore.add_role_to_user(user, 'Doctor')
        db.session.add(user)

        # add as doctor
        doctor = Doctor(name = name, dob = dob, description = description, gender = gender)
        user.user_doctor = doctor
        db.session.commit()

        return marshal(doctor, doctor_fields), 201
    
    def get(self, doctor_id):
        doctor = Doctor.query.filter(Doctor.doctor_id == doctor_id).first()
        if not doctor:
            return "Doctor does not exists", 404

        # base data, this will always be sent
        doctor_data = marshal(doctor, doctor_fields)        

        # flag to see if appointments of this particular doctor is required
        args = get_parser.parse_args()
        flag1 = args.get('upcoming_appointment')
        flag2 = args.get('past_appointment')
        flag3 = args.get('availability')

        if (flag1 == None) and (flag2 == None) and (flag3 == None): 
            return doctor_data, 200
        
        # doctor availability for the coming dates
        da_list = []
        da = doctor.doctor_shift
        for a in da:
            if a.date >= date.today():
                da_list += [a]
        doctor_data['availability'] = marshal(da_list, shift_fields)

        # only return base data and availability 
        if (flag1 == None) and (flag2 == None) and (flag3):
            return doctor_data, 200

        # this doctor's past appointments
        past_apt = Appointment.query.filter(Appointment.doctor_id == doctor_id, Appointment.date < date.today()).all()
        doctor_data['past_appointment'] = marshal(past_apt, appointment_fields)

        # this doctor's upcoming appointments
        upcoming_apt = Appointment.query.filter(Appointment.doctor_id == doctor_id, Appointment.date >= date.today()).all()
        doctor_data['upcoming_appointment'] = marshal(upcoming_apt, appointment_fields)

        return doctor_data, 200

    def delete(self, doctor_id):
        doctor = Doctor.query.filter(Doctor.doctor_id == doctor_id).first()
        if doctor:
            db.session.delete(doctor)
            db.session.commit()
            return 200
        return "Doctor does not exists", 404
    
    def patch(self, doctor_id):
        doctor = Doctor.query.filter(Doctor.doctor_id == doctor_id).first()
        if not doctor:
            return "Doctor does not exists", 404

        data = request.get_json()
        for key in data:
            # check if DOB is updated
            if key == 'dob' and data[key]:
                try:
                    dob = datetime.strptime(data[key], '%d-%m-%Y')
                except:
                    dob = datetime.strptime(data[key], '%Y-%m-%d')
                setattr(doctor, key, dob)

            # check if the doctor is blacklisted
            if key == 'blacklist':
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
                setattr(doctor, key, data[key])
        db.session.commit()
        return marshal(doctor, doctor_fields)
    
class AllDoctorResources(Resource):
    def get(self):
        args = get_parser.parse_args()
        flag = args.get('limit')
        if flag == None:
            all_doctors = Doctor.query.all()
        return marshal(all_doctors, doctor_fields), 200