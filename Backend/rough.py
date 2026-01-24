from app import *
from models import *
from datetime import time, date

# add shifts to hospital
date_today = date.today()
list_of_next_7_dates = [(date_today + timedelta(days = i)) for i in range(8)]
for d in list_of_next_7_dates:
    # print(d)
    s1 = Shift(date = d, name = 'Morning',start_time = datetime(year = d.year, month = d.month, day = d.day, hour=9), end_time = datetime(year = d.year, month = d.month, day = d.day, hour = 12))
    s2 = Shift(date = d, name = 'Afternoon',start_time = datetime(year = d.year, month = d.month, day = d.day, hour=14), end_time = datetime(year = d.year, month = d.month, day = d.day, hour = 17))
    s3 = Shift(date = d, name = 'Evening',start_time = datetime(year = d.year, month = d.month, day = d.day, hour=20), end_time = datetime(year = d.year, month = d.month, day = d.day, hour = 23))

    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)

# provide availability of doctor
a1 = DoctorAvailability(doctor_id = 1, shift_id = 1)
db.session.add(a1)

# patient select slot
a1 = Shift.query.filter(Shift.id == 1).first()
a1 = a1.date
s1 = Slots(date = a1, start_time = datetime(year = a1.year, month = a1.month, day = a1.day,hour = 9), end_time = datetime(year = a1.year, month = a1.month, day = a1.day,hour = 9, minute = 15),
           doctor_id = 1, patient_id = 1)
s1.slots_app = Appointment(date = a1, start_time = datetime(year = a1.year, month = a1.month, day = a1.day, hour = 9), end_time = datetime(year = a1.year, month = a1.month, day = a1.day, hour = 9, minute = 15),
           doctor_id = 1, patient_id = 1)
db.session.add(s1)
db.session.commit()

a = Appointment.query.first()
print(datetime.strftime(a.date, '%d-%m-%Y'))
print(datetime.strftime(a.date, '%H-%M'))