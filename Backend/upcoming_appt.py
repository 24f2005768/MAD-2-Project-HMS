from app import *
from models import *
from datetime import time, date, timedelta
import random

past_week_dates = []

date_today = date.today()
time = datetime.min.time()
date_today = datetime.combine(date_today, time)

next_week_dates = [(date_today + timedelta(days = i)) for i in range(1,8)]

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


today_shift = Shift.query.filter(Shift.date == date_today).all()
next_week_dates = [(date_today + timedelta(days = i)) for i in range(1,8)]
tomorrow_shift = Shift.query.filter(Shift.date == next_week_dates[0]).all()
day_after_tomorrow_shift = Shift.query.filter(Shift.date == next_week_dates[1]).all()

'''
doctor = db.get_or_404(Doctor, 2)

# To get all shifts for a doctor
doctor_shifts = doctor.doctor_shift  # List of Shift objects

# Today shifts
shift1 = today_shift[1]
shift2 = today_shift[2]

# Next week shifts
shift3 = tomorrow_shift[0]
shift4 = tomorrow_shift[2]

shift5 = day_after_tomorrow_shift[0]
shift6 = day_after_tomorrow_shift[1]
# doctors_in_shift = shift.shift_doctor  # List of Doctor objects

# To add a doctor to a shift (either way works)
if shift1 not in doctor.doctor_shift:
    doctor.doctor_shift.append(shift1)

if shift2 not in doctor.doctor_shift:
    doctor.doctor_shift.append(shift2)

if shift3 not in doctor.doctor_shift:
    doctor.doctor_shift.append(shift3)

if shift4 not in doctor.doctor_shift:
    doctor.doctor_shift.append(shift4)

if shift5 not in doctor.doctor_shift:
    doctor.doctor_shift.append(shift5)

if shift6 not in doctor.doctor_shift:
    doctor.doctor_shift.append(shift6)

for a in doctor.doctor_shift:
    check_existing_slots = Slots.query.filter(Slots.shift_id == a.id).all()
    if check_existing_slots == []:
        start_time = a.start_time
        end_time = a.end_time

        while start_time != end_time:
            new_time = timedelta(minutes=15) + start_time
            new_slot = Slots(date = a.date, start_time = start_time, end_time = new_time, doctor_id = doctor.doctor_id, shift_id = a.id)
            db.session.add(new_slot)
            start_time = new_time

db.session.commit()
'''

doctors = Doctor.query.all()
for i in range(len(doctors)):
    doctor = doctors[i]
    # today
    for j in range(2):
        t = random.choice(today_shift)
        today_shift.remove(t)
        print(doctors[i], t)
        if t not in doctor.doctor_shift:
            doctor.doctor_shift.append(t)

    # tomorrow
    for k in range(2):
        t2 = random.choice(tomorrow_shift)
        tomorrow_shift.remove(t2)
        print(doctors[i], t2)
        if t2 not in doctor.doctor_shift:
            doctor.doctor_shift.append(t2)

    # day after tomorrow
    for l in range(2):
        t3 = random.choice(day_after_tomorrow_shift)
        day_after_tomorrow_shift.remove(t3)
        print(doctors[i], t3)
        if t3 not in doctor.doctor_shift:
            doctor.doctor_shift.append(t3)

    print()

    for a in doctor.doctor_shift:
        check_existing_slots = Slots.query.filter(Slots.shift_id == a.id, Slots.doctor_id == doctor.doctor_id).all()
        if check_existing_slots == []:
            start_time = a.start_time
            end_time = a.end_time

            while start_time != end_time:
                new_time = timedelta(minutes=15) + start_time
                new_slot = Slots(date = a.date, start_time = start_time, end_time = new_time, doctor_id = doctor.doctor_id, shift_id = a.id)
                db.session.add(new_slot)
                start_time = new_time

    # reset shifts lists for the next doctor
    today_shift = Shift.query.filter(Shift.date == date_today).all()
    tomorrow_shift = Shift.query.filter(Shift.date == next_week_dates[0]).all()
    day_after_tomorrow_shift = Shift.query.filter(Shift.date == next_week_dates[1]).all()
db.session.commit()

