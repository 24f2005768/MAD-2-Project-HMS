from app import *
from models import *
from datetime import time, date, timedelta, datetime
from sqlalchemy import or_, desc, asc
from datetime import datetime

'''
# Get current local date and time
now = datetime.now()
# print(now.strftime('%B')) # Output: 2026-04-01 10:53:15.123456

patient = db.get_or_404(Patient, 2)
all_appointments = Appointment.query.filter(Appointment.patient_id == patient.patient_id).order_by(Appointment.date).all()

results = {"overall_appt_by_dept": {}, "overall_appt_by_doctors": {}, 
           "this_month_appt_by_dept": {}, "this_month_appt_by_doctors": {},
           "appointments_by_month": {}}

overall_appt_by_dept = {}
overall_appt_by_doctors = {}
this_month_appt_by_dept = {}
this_month_appt_by_doctors = {}
appointments_by_month = {}

this_month_appt = []

# query all depts
depts = Department.query.all()
for d in depts:
    overall_appt_by_dept[d.name] = 0
    this_month_appt_by_dept[d.name] = 0

# query all doctors
doctors = Doctor.query.all()
for doc in doctors:
    overall_appt_by_doctors[doc.name] = 0
    this_month_appt_by_doctors[doc.name] = 0

# appt_by_doc & appt_by_dept overall
for appt in all_appointments:
    # this month's appts
    if appt.date.strftime('%B') == now.strftime('%B'):
        this_month_appt += [appt]

    # separate appointments by departments
    dept = appt.app_doctor.dept.name
    overall_appt_by_dept[dept] += 1

    # separate appointments by doctors
    doc = appt.app_doctor.name
    overall_appt_by_doctors[doc] += 1

    # store month wise trends for this patient's appointments
    if appt.date.strftime('%B') not in appointments_by_month.keys():
        appointments_by_month[appt.date.strftime('%B')] = 1
    else:
        appointments_by_month[appt.date.strftime('%B')] += 1


# appt_by_doc & appt_by_dept for this month
for appt in this_month_appt:
    # separate appointments by departments
    dept = appt.app_doctor.dept.name
    this_month_appt_by_dept[dept] += 1

    # separate appointments by doctors
    doc = appt.app_doctor.name
    this_month_appt_by_doctors[doc] += 1

results["overall_appt_by_dept"] = overall_appt_by_dept
results["overall_appt_by_doctors"] = overall_appt_by_doctors
results["this_month_appt_by_dept"] = this_month_appt_by_dept
results["this_month_appt_by_doctors"] = this_month_appt_by_doctors
results["appointments_by_month"] = appointments_by_month

print(results)
'''

today_appt = Appointment.query.filter(Appointment.date == date.today()).all()
patients_dict = {}
for a in today_appt:
    if a.patient_id not in patients_dict.keys():
        patients_dict[a.patient_id] = {}
        patients_dict[a.patient_id]["appointments"] = [a]
    else:
        patients_dict[a.patient_id]["appointments"] += [a]

for p in patients_dict:
    l = len(patients_dict[p]["appointments"])
    message = f"Hi, you have {l} appointments today"
    patients_dict[p]["message"] = message

doctor = db.get_or_404(Doctor, 2)
prev_month_dates = [(date.today() + timedelta(days = -i)) for i in range(32)]
prev_month_appt = []
for d in prev_month_dates:
    prev_month_appt += Appointment.query.filter(Appointment.date == d, Appointment.doctor_id == doctor.doctor_id).all()
