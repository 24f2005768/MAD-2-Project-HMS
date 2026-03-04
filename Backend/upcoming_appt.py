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
next_week_dates
shift2 = db.get_or_404(Shift, 2)
shift3 = db.get_or_404(Shift, 7)
shift4 = db.get_or_404(Shift, 8)
# doctors_in_shift = shift.shift_doctor  # List of Doctor objects

# To add a doctor to a shift (either way works)
doctor.doctor_shift.append(shift1)
doctor.doctor_shift.append(shift2)
doctor.doctor_shift.append(shift3)
doctor.doctor_shift.append(shift4)

for a in doctor.doctor_shift:
    start_time = a.start_time
    end_time = a.end_time

    while start_time != end_time:
        new_time = timedelta(minutes=15) + start_time
        new_slot = Slots(date = a.date, start_time = start_time, end_time = end_time, doctor_id = doctor.doctor_id, shift_id = a.id)
        # db.session.add(new_slot)
        start_time = new_time

'''

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
# db.session.commit()





'''
# upcoming_appointments.py
import random
from datetime import datetime, date, timedelta
from app import db
from models import Doctor, Patient, Appointment, Shift

# Get all doctors and patients
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

# Time slots for appointments (15 min intervals)
time_slots = [
    (9, 0), (9, 15), (9, 30), (9, 45), 
    (10, 0), (10, 15), (10, 30), (10, 45), 
    (11, 0), (11, 15), (11, 30), (11, 45),
    (14, 0), (14, 15), (14, 30), (14, 45), 
    (15, 0), (15, 15), (15, 30), (15, 45), 
    (16, 0), (16, 15), (16, 30), (16, 45)
]

# Get next 7 days dates
date_today = date.today()
next_week_dates = [date_today + timedelta(days=i) for i in range(1, 8)]

def is_doctor_available(doctor, appointment_date, start_time):
    """Check if doctor has a shift at this date and time"""
    # Get all shifts for this doctor
    doctor_shifts = doctor.doctor_shift
    
    for shift in doctor_shifts:
        # Check if shift is on the same date
        if shift.date.date() == appointment_date:
            # Check if appointment time falls within shift hours
            shift_start = shift.start_time.time()
            shift_end = shift.end_time.time()
            appointment_time = start_time.time()
            
            # Convert to comparable format
            if shift_start <= appointment_time <= shift_end:
                return True
    
    return False

# Create 30 upcoming appointments
appointments_created = 0
max_attempts = 200  # Increased attempts since we have more constraints
attempts = 0

while appointments_created < 30 and attempts < max_attempts:
    attempts += 1
    
    # Randomly select date and time
    d = random.choice(next_week_dates)
    hour, minute = random.choice(time_slots)
    start_time = datetime.combine(d, datetime.min.time()) + timedelta(hours=hour, minutes=minute)
    end_time = start_time + timedelta(minutes=15)
    
    # Randomly select doctor based on specialty
    doctor = random.choice(all_doctors)
    
    # First check if doctor is available at this time (from doctor_availability table)
    if not is_doctor_available(doctor, d, start_time):
        continue  # Doctor doesn't have a shift at this time
    
    # Select patient based on doctor type
    if doctor.doctor_id in [3, 4]:  # Pediatric doctors
        patient = random.choice(pediatric_patients)
    else:  # General doctors
        patient = random.choice(general_patients)
    
    # Check if this patient already has an appointment on this date and time
    patient_busy = Appointment.query.filter(
        Appointment.patient_id == patient.patient_id,
        Appointment.date == d,
        Appointment.start_time == start_time
    ).first()
    
    # Check if doctor already has an appointment at this time
    doctor_busy = Appointment.query.filter(
        Appointment.doctor_id == doctor.doctor_id,
        Appointment.date == d,
        Appointment.start_time == start_time
    ).first()
    
    if not patient_busy and not doctor_busy:
        # Create the appointment (no treatment data for upcoming)
        appointment = Appointment(
            date=d, 
            start_time=start_time, 
            end_time=end_time, 
            status='Booked',  # 'Booked' instead of 'Completed' for upcoming
            doctor_id=doctor.doctor_id, 
            patient_id=patient.patient_id
        )
        
        db.session.add(appointment)
        appointments_created += 1
        
        if appointments_created % 10 == 0:
            print(f"Created {appointments_created} appointments...")
            db.session.commit()

# Final commit
db.session.commit()
print(f"Successfully created {appointments_created} upcoming appointments!")
'''