from flask import current_app
from flask_security.utils import hash_password
from datetime import date, timedelta, time
import random

from app import *
from models import *

past_dates = []
date_today = date.today()
past_dates = [(date_today + timedelta(days = -i)) for i in range(1,90)]

datastore = current_app.datastore

# Patients
user1 = datastore.create_user(user_name = 'Shr_arya', user_password = hash_password('arya'), contact_number = '1783731407', email = 'a@gmail.com')
datastore.add_role_to_user(user1, 'Patient')
user1.user_patient = Patient(name = 'Arya Sharma', dob = date(2007, 10, 3), gender = 'Male', height = 186, weight = 65)
db.session.add(user1)

user2 = datastore.create_user(user_name = 'littledeer', user_password = hash_password('kriti'), contact_number = '9636972612', email = 'k@gmail.com')
datastore.add_role_to_user(user2, 'Patient')
user2.user_patient = Patient(name = 'Kriti Tiwari', dob = date(2004, 9, 18), gender = 'Female', height = 163, weight = 50)
db.session.add(user2)

user3 = datastore.create_user(user_name='Saroj',user_password=hash_password('saroj'),contact_number='5865194463',email='s@email.com')
datastore.add_role_to_user(user3, 'Patient')
user3.user_patient = Patient(name='Saroj Mishra',dob=date(1976, 6, 22),gender='Female',height='162',weight='75')
db.session.add(user3)

user4 = datastore.create_user(user_name='Aadi',user_password=hash_password('aaditya'),contact_number='8030974434',email='a@email.com')
datastore.add_role_to_user(user4, 'Patient')
user4.user_patient = Patient(name='Aadi Trivedi',dob=date(2005, 10, 4),gender='Male',height='183',weight='64')
db.session.add(user4)

user5 = datastore.create_user(user_name='Shruti',user_password=hash_password('shruti'),contact_number='2155059723',email='sh@email.com')
datastore.add_role_to_user(user5, 'Patient')
user5.user_patient = Patient(name='Shruti Hasan',dob=date(2001, 8, 10),gender='Female',height='170',weight='65')
db.session.add(user5)

user6 = datastore.create_user(user_name='Dheeraj',user_password=hash_password('dheeraj'),contact_number='5207633762',email='dc@gmail.com')
datastore.add_role_to_user(user6, 'Patient')
user6.user_patient = Patient(name='Dheeraj Chauhan',dob=date(1984, 3, 11),gender='Male',height='155',weight='52')
db.session.add(user6)

user7 = datastore.create_user(user_name='Jason',user_password=hash_password('jason'),contact_number='4240629978',email='jp@gmail.com')
datastore.add_role_to_user(user7, 'Patient')
user7.user_patient = Patient(name='Jason Perry',dob=date(2013, 4, 13),gender='Male',height='166',weight='68')
db.session.add(user7)

user8 = datastore.create_user(user_name='Tom',user_password=hash_password('tommy'),contact_number='9355035218',email='th@gmail.com')
datastore.add_role_to_user(user8, 'Patient')
user8.user_patient = Patient(name='Tom Hilfiger',dob=date(2003, 5, 4),gender='Male',height='175',weight='98')
db.session.add(user8)

user9 = datastore.create_user(user_name='Viena',user_password=hash_password('viena'),contact_number='9576063488',email='vs@gmail.com')
datastore.add_role_to_user(user9, 'Patient')
user9.user_patient = Patient(name='Viena Skye',dob=date(1994, 10, 7),gender='Female',height='140',weight='70')
db.session.add(user9)

# Pediatrics patients
user10 = datastore.create_user(user_name='Kashish',user_password=hash_password('kashish'),contact_number='1149508564',email='km@gmail.com')
datastore.add_role_to_user(user10, 'Patient')
user10.user_patient = Patient(name='Kashish Mathur',dob=date(2014, 11, 6),gender='Female',height='149',weight='82')
db.session.add(user10)

user11 = datastore.create_user(user_name='Rudraksh',user_password=hash_password('rudraksh'),contact_number='3127523027',email='rp@gmail.com')
datastore.add_role_to_user(user11, 'Patient')
user11.user_patient = Patient(name='Rudraksh Patel',dob=date(2024, 9, 4),gender='Male',height='56',weight='4.5')
db.session.add(user11)

user12 = datastore.create_user(user_name='Vipul',user_password=hash_password('vipul'),contact_number='1024037587',email='vr@gmail.com')
datastore.add_role_to_user(user12, 'Patient')
user12.user_patient = Patient(name='Vipul Raj',dob=date(2010, 1, 4),gender='Male',height='130',weight='48')
db.session.add(user12)

user13 = datastore.create_user(user_name='Anamika',user_password=hash_password('anamika'),contact_number='9040428872',email='as@gmail.com')
datastore.add_role_to_user(user13, 'Patient')
user13.user_patient = Patient(name='Anamika Sen',dob=date(2018, 7, 30),gender='Female',height='100',weight='25')
db.session.add(user13)

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

doctor1 = db.session.get(Doctor, 1)
doctor2 = db.session.get(Doctor, 2)
doctor3 = db.session.get(Doctor, 3)
doctor4 = db.session.get(Doctor, 4)
doctor5 = db.session.get(Doctor, 5)
doctor6 = db.session.get(Doctor, 6)

patient1 = db.session.get(Patient, 1)
patient2 = db.session.get(Patient, 2) 
patient3 = db.session.get(Patient, 3)
patient4 = db.session.get(Patient, 4)
patient5 = db.session.get(Patient, 5)
patient6 = db.session.get(Patient, 6) 
patient7 = db.session.get(Patient, 7)
patient8 = db.session.get(Patient, 8) 
patient9 = db.session.get(Patient, 9)
patient10 = db.session.get(Patient, 10)
patient11 = db.session.get(Patient, 11)
patient12 = db.session.get(Patient, 12)
patient13 = db.session.get(Patient, 13)

general_patients = [patient1, patient2, patient3, patient4, patient5, patient6, patient8, patient9]
pediatric_patients = [patient7, patient10, patient11, patient12, patient13]
all_doctors = [doctor1, doctor2, doctor3, doctor4, doctor5, doctor6]

time_slots = [
    (9, 0), (9, 15), (9, 30), (9, 45), 
    (10, 0), (10, 15), (10, 30), (10, 45), 
    (11, 0), (11, 15), (11, 30), (11, 45),
    (14, 0), (14, 15), (14, 30), (14, 45), 
    (15, 0), (15, 15), (15, 30), (15, 45), 
    (16, 0), (16, 15), (16, 30), (16, 45),
    (20, 0), (20, 15), (20, 30), (20, 45), 
    (21, 0), (21, 15), (21, 30), (21, 45), 
    (22, 0), (22, 15), (22, 30), (22, 45)
]

for i in range(250):
    d = random.choice(past_dates)
    hour, minute = random.choice(time_slots)
    start_time = datetime(year=d.year, month=d.month, day=d.day, hour=hour, minute=minute)
    end_time = start_time + timedelta(minutes=15)
    
    # select a doctor
    doctor = random.choice(all_doctors)
    
    if doctor.doctor_id in [3, 4]:  # Pediatric doctors
        patient = random.choice(pediatric_patients)
    else:
        patient = random.choice(general_patients)
    
    appointment = Appointment(date=d, start_time=start_time, end_time=end_time, status='Completed', doctor_id=doctor.doctor_id, patient_id=patient.patient_id)
    
    appointment.app_t = Treatment(diagnosis='Some diagnosis from doctor', notes='Some notes from doctor', prescription='Some prescription from doctor', tests='Some tests from doctor')
    db.session.add(appointment)

# Profile Pictures
p1 = ProfilePictures(role = "Patient", name = "boy")
p2 = ProfilePictures(role = "Patient", name = "girl")
p3 = ProfilePictures(role = "Patient", name = "male_patient")
p4 = ProfilePictures(role = "Patient", name = "female_patient")
p5 = ProfilePictures(role = "Doctor", name = "FemaleDoctor")
p6 = ProfilePictures(role = "Doctor", name = "MaleDoctor")
p7 = ProfilePictures(role = "Department", name = "Cardiology")
p8 = ProfilePictures(role = "Department", name = "Gastrology")
p9 = ProfilePictures(role = "Department", name = "General Surgery")
p10 = ProfilePictures(role = "Department", name = "Pediatrics")

lst = [p1,p2,p3,p4,p4,p5,p6,p7,p8,p9,p10]
for p in lst:
    db.session.add(p)

pics = ProfilePictures.query.all()

# for departments
depts = Department.query.all()

for d in depts:
    for p in pics:
        if d.name == p.name:
            d.pfp = p.name

# for doctors
doc = Doctor.query.all()

for d in doc:
    if d.gender == 'Female':
        d.pfp = p5.name
    else:
        d.pfp = p6.name

# for patients
patients = Patient.query.all()

for p in patients:
    # for underage patients
    if p.get_age_in_years() < 18:
        if p.gender == 'Female':
            p.pfp = p2.name
        else:
            p.pfp = p1.name
    else:
        if p.gender == "Female":
            p.pfp = p4.name
        else:
            p.pfp = p3.name

db.session.commit()