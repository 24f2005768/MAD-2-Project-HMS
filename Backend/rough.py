from app import *
from models import *
from datetime import time, date, timedelta

past_week_dates = []
date_today = date.today()
past_week_dates = [(date_today + timedelta(days = -i)) for i in range(1,8)]

doctor = db.get_or_404(Doctor, 1)

# '''
# add shifts to hospital
date_today = date.today()
list_of_next_7_dates = [(date_today + timedelta(days = i)) for i in range(8)]
for d in list_of_next_7_dates:
    s1 = Shift(date = d, name = 'Morning',start_time = datetime(year = d.year, month = d.month, day = d.day, hour=9), end_time = datetime(year = d.year, month = d.month, day = d.day, hour = 12))
    s2 = Shift(date = d, name = 'Afternoon',start_time = datetime(year = d.year, month = d.month, day = d.day, hour=14), end_time = datetime(year = d.year, month = d.month, day = d.day, hour = 17))
    s3 = Shift(date = d, name = 'Evening',start_time = datetime(year = d.year, month = d.month, day = d.day, hour=20), end_time = datetime(year = d.year, month = d.month, day = d.day, hour = 23))

    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)

# To get all shifts for a doctor
doctor_shifts = doctor.doctor_shift  # List of Shift objects

# To get all doctors for a shift
shift1 = db.get_or_404(Shift, 1)
shift2 = db.get_or_404(Shift, 2)
shift3 = db.get_or_404(Shift, 7)
shift4 = db.get_or_404(Shift, 8)
# doctors_in_shift = shift.shift_doctor  # List of Doctor objects

# To add a doctor to a shift (either way works)
doctor.doctor_shift.append(shift1)
doctor.doctor_shift.append(shift2)
doctor.doctor_shift.append(shift3)
doctor.doctor_shift.append(shift4)

'''
# provide availability of doctor
# today
a1 = DoctorAvailability(doctor_id = 1, shift_id = 1)
a2 = DoctorAvailability(doctor_id = 1, shift_id = 3)

# next week
a3 = DoctorAvailability(doctor_id = 1, shift_id = 7)
a4 = DoctorAvailability(doctor_id = 1, shift_id = 8)
a5 = DoctorAvailability(doctor_id = 1, shift_id = 13)
a6 = DoctorAvailability(doctor_id = 1, shift_id = 14)
a7 = DoctorAvailability(doctor_id = 1, shift_id = 19)
a8 = DoctorAvailability(doctor_id = 1, shift_id = 20)

db.session.add(a1)
db.session.add(a2)
db.session.add(a3)
db.session.add(a4)
db.session.add(a5)
db.session.add(a6)
db.session.add(a7)
db.session.add(a8)

# populate Slots table
av1 = Shift.query.filter(Shift.id == 3).first()
start_time = av1.start_time
end_time = av1.end_time

while start_time != end_time:
    new_time = timedelta(minutes = 15) + start_time
    new_slot = Slots(date = av1.date, start_time = start_time, end_time = new_time, doctor_id = 1)
    db.session.add(new_slot)
    start_time = new_time

today_booking1 = Slots.query.filter(Slots.id == 2).first()
today_booking2 = Slots.query.filter(Slots.id == 7).first()

# Book an appointment for patient
today_booking1.patient_id = 2
today_booking2.patient_id = 1

add_app1 = Appointment(date = today_booking1.date, start_time = today_booking1.start_time, end_time = today_booking1.end_time, 
                       slot_id = today_booking1.id, doctor_id = 1, patient_id = 2, status = 'Booked')
add_app2 = Appointment(date = today_booking1.date, start_time = today_booking1.start_time, end_time = today_booking1.end_time, 
                       slot_id = today_booking1.id, doctor_id = 1, patient_id = 1, status = 'Booked')

db.session.add(add_app1)
db.session.add(add_app2)
'''
db.session.commit()
