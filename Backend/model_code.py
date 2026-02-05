from flask import current_app
from flask_security.utils import hash_password
from datetime import date, timedelta, time

from app import *
from models import *

past_week_dates = []
date_today = date.today()
past_week_dates = [(date_today + timedelta(days = -i)) for i in range(1,8)]

datastore = current_app.datastore

# Patients
user1 = datastore.create_user(user_name = 'Shr_arya', user_password = hash_password('aryaa'), contact_number = '1783731407', email = 'a@gmail.com')
datastore.add_role_to_user(user1, 'Patient')
user1.user_patient = Patient(name = 'Arya Sharma', dob = date(2007, 10, 3), gender = 'Male', height = 186, weight = 65)
db.session.add(user1)

user2 = datastore.create_user(user_name = 'littledeer', user_password = hash_password('kriti'), contact_number = '9636972612', email = 'k@gmail.com')
datastore.add_role_to_user(user2, 'Patient')
user2.user_patient = Patient(name = 'Kriti Tiwari', dob = date(2004, 9, 18), gender = 'Female', height = 163, weight = 50)
db.session.add(user2)

# Doctors 
user1 = datastore.create_user(user_name = 'Ganesh_heart', user_password = hash_password('ganesh'), contact_number = '5746160792', email = 'g@email.com')
datastore.add_role_to_user(user1, 'Doctor')
user1.user_doctor = Doctor(name = 'Ganesh Rathi', gender = 'Male', dob = date(1978, 3, 12), department_id = 1)
db.session.add(user1)

user2 = datastore.create_user(user_name = 'Vignesh_heart', user_password = hash_password('vignesh'), contact_number = '8166956143', email = 'v@email.com')
datastore.add_role_to_user(user2, 'Doctor')
user2.user_doctor = Doctor(name = 'Vignesh Kumar', gender = 'Male', dob = date(1966, 2, 14), department_id = 1)
db.session.add(user2)

user3 = datastore.create_user(user_name = 'Preeti_pediatrics', user_password = hash_password('preeti'), contact_number = '9370595052', email = 'p@email.com')
datastore.add_role_to_user(user3, 'Doctor')
user3.user_doctor = Doctor(name = 'Preeti Rai', gender = 'Female', dob = date(1988, 3, 17), department_id = 2)
db.session.add(user3)

user4 = datastore.create_user(user_name = 'Rajkumar_pediatrics', user_password = hash_password('rajkumar'), contact_number = '7996673737', email = 'p@email.com')
datastore.add_role_to_user(user4, 'Doctor')
user4.user_doctor = Doctor(name = 'Rajkumar Desai', gender = 'Male', dob = date(1973, 5, 8), department_id = 2)
db.session.add(user4)

user5 = datastore.create_user(user_name = 'Devanand_surgery', user_password = hash_password('devanand'), contact_number = '1059832795', email = 'd@email.com')
datastore.add_role_to_user(user5, 'Doctor')
user5.user_doctor = Doctor(name = 'Devanand Sharma', gender = 'Male', dob = date(1998, 4, 10), department_id = 3)
db.session.add(user5)

user6 = datastore.create_user(user_name = 'Vikas_surgery', user_password = hash_password('vikas'), contact_number = '2073880656', email = 'vs@email.com')
datastore.add_role_to_user(user6, 'Doctor')
user6.user_doctor = Doctor(name = 'Vikas Jindal', gender = 'Male', dob = date(1980, 6, 12), department_id = 3)
db.session.add(user6)

# Departments
dept1 = Department(name = 'Cardiology')
db.session.add(dept1)

dept2 = Department(name = 'Pediatrics')
db.session.add(dept2)

dept3 = Department(name = 'General Surgery')
db.session.add(dept3)

dept4 = Department(name = 'Gastrology')
db.session.add(dept4)

# Past Appointments

patient1 = db.get_or_404(Patient, 1)
patient2 = db.get_or_404(Patient, 2)

doctor1 = db.get_or_404(Doctor, 1)

d = past_week_dates[1]
apt1 = Appointment(date = d, start_time = datetime(year = d.year, month = d.month, day = d.day, hour = 9), 
                   end_time = datetime(year = d.year, month = d.month, day = d.day, hour = 9, minute = 15),
                   status = 'Completed', doctor_id = doctor1.doctor_id, patient_id = patient2.patient_id)
apt1.app_t = Treatment(diagnosis = 'Some diagnosis from doctor', notes = 'Some notes from doctor', prescription = 'Some prescription from doctor', tests = 'Some tests from doctor')
db.session.add(apt1)

d = past_week_dates[2]
apt2 = Appointment(date = d, start_time = datetime(year = d.year, month = d.month, day = d.day, hour = 9, minute = 45), 
                   end_time = datetime(year = d.year, month = d.month, day = d.day, hour = 10),
                   status = 'Completed', doctor_id = doctor1.doctor_id, patient_id = patient1.patient_id)
apt2.app_t = Treatment(diagnosis = 'Some diagnosis from doctor', notes = 'Some notes from doctor', prescription = 'Some prescription from doctor', tests = 'Some tests from doctor')
db.session.add(apt2)

d = past_week_dates[4]
apt3 = Appointment(date = d, start_time = datetime(year = d.year, month = d.month, day = d.day, hour = 11), 
                   end_time = datetime(year = d.year, month = d.month, day = d.day, hour = 11, minute = 15),
                   status = 'Completed', doctor_id = doctor1.doctor_id, patient_id = patient2.patient_id)
apt3.app_t = Treatment(diagnosis = 'Some diagnosis from doctor', notes = 'Some notes from doctor', prescription = 'Some prescription from doctor', tests = 'Some tests from doctor')
db.session.add(apt3)


db.session.commit()