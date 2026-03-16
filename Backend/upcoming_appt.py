from app import *
from models import *
from datetime import time, date, timedelta

past_week_dates = []

date_today = date.today()
time = datetime.min.time()
date_today = datetime.combine(date_today, time)

next_week_dates = [(date_today + timedelta(days = i)) for i in range(1,8)]

doctor = db.get_or_404(Doctor, 2)

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

# To get all shifts for a doctor
doctor_shifts = doctor.doctor_shift  # List of Shift objects

today_shift = Shift.query.filter(Shift.date == date_today).all()

# Today shifts
shift1 = today_shift[1]
shift2 = today_shift[2]

# Next week shifts
next_week_dates = [(date_today + timedelta(days = i)) for i in range(1,8)]
tomorrow_shift = Shift.query.filter(Shift.date == next_week_dates[0]).all()
shift3 = tomorrow_shift[0]
shift4 = tomorrow_shift[2]

day_after_tomorrow_shift = Shift.query.filter(Shift.date == next_week_dates[1]).all()
shift5 = day_after_tomorrow_shift[0]
shift6 = day_after_tomorrow_shift[1]
# doctors_in_shift = shift.shift_doctor  # List of Doctor objects

# To add a doctor to a shift (either way works)
doctor.doctor_shift.append(shift1)
doctor.doctor_shift.append(shift2)
doctor.doctor_shift.append(shift3)
doctor.doctor_shift.append(shift4)
doctor.doctor_shift.append(shift5)
doctor.doctor_shift.append(shift6)

for a in doctor.doctor_shift:
    start_time = a.start_time
    end_time = a.end_time

    while start_time != end_time:
        new_time = timedelta(minutes=15) + start_time
        new_slot = Slots(date = a.date, start_time = start_time, end_time = new_time, doctor_id = doctor.doctor_id, shift_id = a.id)
        db.session.add(new_slot)
        start_time = new_time

# getting slot
# Slots.query.fil

db.session.commit()