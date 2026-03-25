from app import *
from models import *
from datetime import time, date, timedelta, datetime
from sqlalchemy import or_, desc, asc
import random 

# dates = Shift.query.order_by(desc(Shift.id)).all()
# search_query = "23"

patient = db.get_or_404(Patient, 2)
doctor = db.get_or_404(Doctor, 2)
date_today = date.today()
# print(patient.get_age())
# doctor_shift = doctor.doctor_shift

# patient1 = db.session.get(Patient, 1)
# patient2 = db.session.get(Patient, 2) 
# patient3 = db.session.get(Patient, 3)
# patient4 = db.session.get(Patient, 4)
# patient5 = db.session.get(Patient, 5)
# patient6 = db.session.get(Patient, 6) 
# patient7 = db.session.get(Patient, 7)
# patient8 = db.session.get(Patient, 8) 
# patient9 = db.session.get(Patient, 9)
# patient10 = db.session.get(Patient, 10)
# patient11 = db.session.get(Patient, 11)
# patient12 = db.session.get(Patient, 12)
# patient13 = db.session.get(Patient, 13)

# general_patients = [patient1, patient2, patient3, patient4, patient5, patient6, patient8, patient9]
# slot_today = Slots.query.filter(Slots.date == date.today(), Slots.doctor_id == 2).all()
# for i in range(5):
#     s = random.choice(slot_today)
#     patient = random.choice(general_patients)
#     s.patient_id = patient.patient_id
#     appointment = Appointment(date = date.today(), start_time = s.start_time, end_time = s.end_time, status = "Booked", doctor_id = doctor.doctor_id, patient_id = patient.patient_id, slot_id = s.id)
#     db.session.add(appointment)
#     slot_today.remove(s)
#     general_patients.remove(patient)

# general_patients = [patient1, patient2, patient3, patient4, patient5, patient6, patient8, patient9]
# next_week_dates = [(date.today() + timedelta(days = i)) for i in range(1,8)]
# tomorrow_shift = Slots.query.filter(Slots.date == next_week_dates[0], Slots.doctor_id == doctor.doctor_id).all()

# for i in range(5):
#     s = random.choice(tomorrow_shift)
#     patient = random.choice(general_patients)
#     s.patient_id = patient.patient_id
#     appointment = Appointment(date = s.date, start_time = s.start_time, end_time = s.end_time, status = "Booked", doctor_id = doctor.doctor_id, patient_id = patient.patient_id, slot_id = s.id)
#     db.session.add(appointment)
#     tomorrow_shift.remove(s)
#     general_patients.remove(patient)

# general_patients = [patient1, patient2, patient3, patient4, patient5, patient6, patient8, patient9]
# day_after_tomorrow_shift = Slots.query.filter(Slots.date == next_week_dates[1], Slots.doctor_id == doctor.doctor_id).all()

# for i in range(5):
#     s = random.choice(day_after_tomorrow_shift)
#     patient = random.choice(general_patients)
#     s.patient_id = patient.patient_id
#     appointment = Appointment(date = s.date, start_time = s.start_time, end_time = s.end_time, status = "Booked", doctor_id = doctor.doctor_id, patient_id = patient.patient_id, slot_id = s.id)
#     db.session.add(appointment)
#     day_after_tomorrow_shift.remove(s)
#     general_patients.remove(patient)

# db.session.commit()

time = datetime.min.time()
start_d = datetime(year = date_today.year, month=date_today.month, day = 1)
# end_date = datetime.combine(date_today, time)

monthly_appointments = Appointment.query.filter(Appointment.start_time >= start_d, Appointment.patient_id == patient.patient_id).all()
print(monthly_appointments)
