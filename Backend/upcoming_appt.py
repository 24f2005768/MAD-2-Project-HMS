from app import *
from models import *
from datetime import time, date, timedelta

past_week_dates = []

date_today = date.today()
time = datetime.min.time()
date_today = datetime.combine(date_today, time)

next_week_dates = [(date_today + timedelta(days = i)) for i in range(1,8)]

doctor = db.get_or_404(Doctor, 1)
# To get all shifts for a doctor
doctor_shifts = doctor.doctor_shift  # List of Shift objects

today_shift = Shift.query.filter(Shift.date == date_today).all()

# Today shifts
shift1 = today_shift[1]
shift1 = today_shift[2]

# Next week shifts
next_week_dates = [(date_today + timedelta(days = i)) for i in range(1,8)]
tomorrow_shift = Shift.query.filter(Shift.date == next_week_dates[0]).all()
shift2 = tomorrow_shift[0]
shift3 = tomorrow_shift[2]
# doctors_in_shift = shift.shift_doctor  # List of Doctor objects

# To add a doctor to a shift (either way works)
doctor.doctor_shift.append(shift1)
doctor.doctor_shift.append(shift2)
doctor.doctor_shift.append(shift3)

for a in doctor.doctor_shift:
    start_time = a.start_time
    end_time = a.end_time

    while start_time != end_time:
        new_time = timedelta(minutes=15) + start_time
        new_slot = Slots(date = a.date, start_time = start_time, end_time = new_time, doctor_id = doctor.doctor_id, shift_id = a.id)
        db.session.add(new_slot)
        start_time = new_time

db.session.commit()