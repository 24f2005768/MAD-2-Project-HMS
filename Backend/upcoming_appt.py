# from app import *
from models import *
from datetime import time, date, timedelta
import random

date_today = date.today()
time = datetime.min.time()
date_today = datetime.combine(date_today, time)

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

doctors = Doctor.query.all()

def add_doctor_shifts_today():
    doctors = Doctor.query.all()

    date_today = date.today()
    time = datetime.min.time()
    date_today = datetime.combine(date_today, time)

    today_shift = Shift.query.filter(Shift.date == date_today).all()
    
    # add slots for doctors
    for i in range(len(doctors)):
        doctor = doctors[i]

        for j in range(2):
            t = random.choice(today_shift)
            today_shift.remove(t)
            # print(doctors[i], t)
            if t not in doctor.doctor_shift:
                doctor.doctor_shift.append(t)

        for a in doctor.doctor_shift:
            check_existing_slots = Slots.query.filter(Slots.shift_id == a.id, Slots.doctor_id == doctor.doctor_id).all()
            # print(doctor, len(check_existing_slots), a)
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

    # add appointments
    general_doctor_slots_today = Slots.query.filter(Slots.date == date.today(), Slots.doctor_id.in_([1,2,5,6])).all()
    pediatrics_doctor_slots_today = Slots.query.filter(Slots.date == date.today(), Slots.doctor_id.in_([3,4])).all()

    for i in range(50):
        general_patients = [patient1, patient2, patient3, patient4, patient5, patient6, patient8, patient9]
        s = random.choice(general_doctor_slots_today)
        patient = random.choice(general_patients)
        doctor = db.get_or_404(Doctor, s.doctor_id)
        patient_available = Slots.query.filter(Slots.patient_id == patient.patient_id, Slots.start_time == s.start_time, 
                                            Slots.end_time == s.end_time,).all()
        if patient_available == []:
            s.patient_id = patient.patient_id
            appointment = Appointment(date = date.today(), start_time = s.start_time, end_time = s.end_time, status = "Booked", 
                                    doctor_id = doctor.doctor_id, patient_id = patient.patient_id, slot_id = s.id)
            db.session.add(appointment)
            general_doctor_slots_today.remove(s)
            general_patients.remove(patient)
        else:
            pass

    for i in range(20):
        pediatrics_patients = [patient10, patient11, patient12, patient13]
        s = random.choice(pediatrics_doctor_slots_today)
        patient = random.choice(pediatrics_patients)
        doctor = db.get_or_404(Doctor, s.doctor_id)
        patient_available = Slots.query.filter(Slots.patient_id == patient.patient_id, Slots.start_time == s.start_time, 
                                            Slots.end_time == s.end_time,).all()
        if patient_available == []:
            s.patient_id = patient.patient_id
            appointment = Appointment(date = date.today(), start_time = s.start_time, end_time = s.end_time, status = "Booked", 
                                    doctor_id = doctor.doctor_id, patient_id = patient.patient_id, slot_id = s.id)
            db.session.add(appointment)
            pediatrics_doctor_slots_today.remove(s)
            pediatrics_patients.remove(patient)
        else:
            pass
    db.session.commit()
    return True

def add_doctor_shifts_tomorrow():
    doctors = Doctor.query.all()

    date_today = date.today()
    time = datetime.min.time()
    date_today = datetime.combine(date_today, time)

    next_week_dates = [(date_today + timedelta(days = i)) for i in range(1,8)]
    tomorrow_shift = Shift.query.filter(Shift.date == next_week_dates[0]).all()

    # add slots for doctors
    for i in range(len(doctors)):
        doctor = doctors[i]

        for k in range(2):
            t2 = random.choice(tomorrow_shift)
            tomorrow_shift.remove(t2)
            if t2 not in doctor.doctor_shift:
                doctor.doctor_shift.append(t2)

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
        tomorrow_shift = Shift.query.filter(Shift.date == next_week_dates[0]).all()
        
    # add appointments
    tomorrow_date = date.today() + timedelta(days=1)
    general_doctor_slots_tomorrow = Slots.query.filter(Slots.date == tomorrow_date, Slots.doctor_id.in_([1,2,5,6])).all()
    pediatrics_doctor_slots_tomorrow = Slots.query.filter(Slots.date == tomorrow_date, Slots.doctor_id.in_([3,4])).all()

    for i in range(50):
        general_patients = [patient1, patient2, patient3, patient4, patient5, patient6, patient8, patient9]
        s = random.choice(general_doctor_slots_tomorrow)
        patient = random.choice(general_patients)
        doctor = db.get_or_404(Doctor, s.doctor_id)
        patient_available = Slots.query.filter(Slots.patient_id == patient.patient_id, Slots.start_time == s.start_time, 
                                            Slots.end_time == s.end_time,).all()
        if patient_available == []:
            s.patient_id = patient.patient_id
            appointment = Appointment(date = next_week_dates[0], start_time = s.start_time, end_time = s.end_time, status = "Booked", 
                                    doctor_id = doctor.doctor_id, patient_id = patient.patient_id, slot_id = s.id)
            db.session.add(appointment)
            general_doctor_slots_tomorrow.remove(s)
            general_patients.remove(patient)
        else:
            pass

    for i in range(20):
        pediatrics_patients = [patient10, patient11, patient12, patient13]
        s = random.choice(pediatrics_doctor_slots_tomorrow)
        patient = random.choice(pediatrics_patients)
        doctor = db.get_or_404(Doctor, s.doctor_id)
        patient_available = Slots.query.filter(Slots.patient_id == patient.patient_id, Slots.start_time == s.start_time, 
                                            Slots.end_time == s.end_time,).all()
        if patient_available == []:
            s.patient_id = patient.patient_id
            appointment = Appointment(date = next_week_dates[0], start_time = s.start_time, end_time = s.end_time, status = "Booked", 
                                    doctor_id = doctor.doctor_id, patient_id = patient.patient_id, slot_id = s.id)
            db.session.add(appointment)
            pediatrics_doctor_slots_tomorrow.remove(s)
            pediatrics_patients.remove(patient)
        else:
            pass

    db.session.commit()
    return True

def add_doctor_shifts_day_after_tomorrow():
    doctors = Doctor.query.all()

    date_today = date.today()
    time = datetime.min.time()
    date_today = datetime.combine(date_today, time)

    next_week_dates = [(date_today + timedelta(days = i)) for i in range(1,8)]
    day_after_tomorrow_shift = Shift.query.filter(Shift.date == next_week_dates[1]).all()

    for i in range(len(doctors)):
        doctor = doctors[i]

        for l in range(2):
            t3 = random.choice(day_after_tomorrow_shift)
            day_after_tomorrow_shift.remove(t3)
            if t3 not in doctor.doctor_shift:
                doctor.doctor_shift.append(t3)

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
        day_after_tomorrow_shift = Shift.query.filter(Shift.date == next_week_dates[1]).all()

    # add appointments
    day_after_tomorrow_date = date.today() + timedelta(days=2)
    general_doctor_slots_day_after_tommorow = Slots.query.filter(Slots.date == day_after_tomorrow_date, Slots.doctor_id.in_([1,2,5,6])).all()
    pediatrics_doctor_slots_day_after_tommorow = Slots.query.filter(Slots.date == day_after_tomorrow_date, Slots.doctor_id.in_([3,4])).all()

    for i in range(50):
        general_patients = [patient1, patient2, patient3, patient4, patient5, patient6, patient8, patient9]
        s = random.choice(general_doctor_slots_day_after_tommorow)
        patient = random.choice(general_patients)
        doctor = db.get_or_404(Doctor, s.doctor_id)
        patient_available = Slots.query.filter(Slots.patient_id == patient.patient_id, Slots.start_time == s.start_time, 
                                            Slots.end_time == s.end_time,).all()
        if patient_available == []:
            s.patient_id = patient.patient_id
            appointment = Appointment(date = next_week_dates[1], start_time = s.start_time, end_time = s.end_time, status = "Booked", 
                                    doctor_id = doctor.doctor_id, patient_id = patient.patient_id, slot_id = s.id)
            db.session.add(appointment)
            general_doctor_slots_day_after_tommorow.remove(s)
            general_patients.remove(patient)
        else:
            pass

    for i in range(20):
        pediatrics_patients = [patient10, patient11, patient12, patient13]
        s = random.choice(pediatrics_doctor_slots_day_after_tommorow)
        patient = random.choice(pediatrics_patients)
        doctor = db.get_or_404(Doctor, s.doctor_id)
        patient_available = Slots.query.filter(Slots.patient_id == patient.patient_id, Slots.start_time == s.start_time, 
                                            Slots.end_time == s.end_time,).all()
        if patient_available == []:
            s.patient_id = patient.patient_id
            appointment = Appointment(date = next_week_dates[1], start_time = s.start_time, end_time = s.end_time, status = "Booked", 
                                    doctor_id = doctor.doctor_id, patient_id = patient.patient_id, slot_id = s.id)
            db.session.add(appointment)
            pediatrics_doctor_slots_day_after_tommorow.remove(s)
            pediatrics_patients.remove(patient)
        else:
            pass

    db.session.commit()
    return True

date_today = date.today()

# --------------------------------------------------------------- Book Appointments ------------------------------------------------------------------------------
'''

# delete any clashing appointments
appts = Appointment.query.filter(Appointment.status == "Booked").all()
for appt in appts:
    clashing_appts = Appointment.query.filter(Appointment.status == "Booked", Appointment.appointment_id != appt.appointment_id,
                                              Appointment.doctor_id == appt.doctor_id, Appointment.start_time == appt.start_time).all()
    # print(clashing_appts)
    for a in clashing_appts:
        db.session.delete(a)

db.session.commit()

'''