from flask import jsonify, request, current_app
from flask_security import auth_required, roles_required, current_user
from datetime import date, timedelta, time
from flask_restful import Resource, marshal, reqparse
from sqlalchemy import desc

from models import *
from caching_config import cache
from .marshal_fields import doctor_fields, appointment_fields, shift_fields, patient_fields

class AdminChartsResources(Resource):
    @auth_required("token")
    @roles_required("Admin")
    def get(self):
        results = {}
        # Chart1: Show month wise appointments
        appointments = Appointment.query.order_by(Appointment.date).all()
        appointments_by_month = {}
        for appt in appointments:
            if appt.date.strftime('%B') not in appointments_by_month.keys():
                appointments_by_month[appt.date.strftime('%B')] = 1
            else:
                appointments_by_month[appt.date.strftime('%B')] += 1
        results["appointments_by_month"] = appointments_by_month


        # Chart2: Show department wise appointments
        appointments_by_dept = {}
        departments = Department.query.all()
        for dept in departments:
            appointments_by_dept[dept.name] = 0

        for appt in appointments:
            appointments_by_dept[appt.app_doctor.dept.name] += 1
        results["appointments_by_dept"] = appointments_by_dept

        # Chart3: Show department wise distribution of doctors
        doctors_by_dept = {}
        departments = Department.query.all()
        for dept in departments:
            doctors_by_dept[dept.name] = len(dept.doctors)
        results["doctors_by_dept"] = doctors_by_dept

        # Chart4: Show gender distribution of patients
        patients = Patient.query.all()
        patients_by_gender = {"Male": 0, "Female": 0, "Other": 0}
        for patient in patients:
            if patient.gender == "Male":
                patients_by_gender["Male"] += 1
            elif patient.gender == "Female":
                patients_by_gender["Female"] += 1
            else:
                patients_by_gender["Other"] += 1
        results["patients_by_gender"] = patients_by_gender

        # Display counts
        patients = Patient.query.all()
        doctors = Doctor.query.all()
        departments = Department.query.all()
        appointments = Appointment.query.all()

        results["count"] = {"patients": len(patients), "doctors": len(doctors), "departments": len(departments), "appointments": len(appointments)}

        return results, 200
    
class PatientChartsResources(Resource):
    @auth_required("token")
    @roles_required("Patient")
    def get(self, patient_id):

        # Get current local date and time
        now = datetime.now()

        patient = db.get_or_404(Patient, patient_id)
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

        return results, 200 

class DoctorChartsResource(Resource):
    @auth_required("token")
    @roles_required("Doctor")
    def get(self, doctor_id):
        doctor = db.get_or_404(Doctor, doctor_id)

        results = {}

        # Chart1: Show month wise appointments
        patients_set = set()
        appointments = Appointment.query.filter(Appointment.doctor_id == doctor.doctor_id).order_by(Appointment.date).all()
        appointments_by_month = {}
        for appt in appointments:
            if appt.date.strftime('%B') not in appointments_by_month.keys():
                appointments_by_month[appt.date.strftime('%B')] = 1
            else:
                appointments_by_month[appt.date.strftime('%B')] += 1

            # add patient IDs to query for gender wise distribution 
            patients_set.add(appt.patient_id)
        results["appointments_by_month"] = appointments_by_month

        # Chart 2 and 3: Show busiest slots of this doctor {overall, month wise}
        overall_busiest_slots = {"Morning": 0, "Afternoon": 0, "Evening": 0}
        this_month_busiest_slots = {"Morning": 0, "Afternoon": 0, "Evening": 0}

        # Past appointments were not built with proper shift-slot relationship, they are randomly generated
        # Work around to get the shift name
        morning_time_slots = [
            (9, 0), (9, 15), (9, 30), (9, 45), 
            (10, 0), (10, 15), (10, 30), (10, 45), 
            (11, 0), (11, 15), (11, 30), (11, 45),
        ]

        afternoon_time_slots = [
            (14, 0), (14, 15), (14, 30), (14, 45), 
            (15, 0), (15, 15), (15, 30), (15, 45), 
            (16, 0), (16, 15), (16, 30), (16, 45),
        ]

        evening_time_slots = [
            (20, 0), (20, 15), (20, 30), (20, 45), 
            (21, 0), (21, 15), (21, 30), (21, 45), 
            (22, 0), (22, 15), (22, 30), (22, 45)
        ]

        doctor_slots = Appointment.query.filter(Appointment.doctor_id == doctor.doctor_id).all()

        for s in doctor_slots:
            # build a start_time tuple
            start_time = (s.start_time.hour, s.start_time.minute)

            # add to respective overall lists
            if start_time in morning_time_slots:
                overall_busiest_slots["Morning"] += 1
            elif start_time in afternoon_time_slots:
                overall_busiest_slots["Afternoon"] += 1
            elif start_time in evening_time_slots:
                overall_busiest_slots["Evening"] += 1

            # add to respective month wise lists
            if start_time in morning_time_slots and s.date.month == date.today().month:
                this_month_busiest_slots["Morning"] += 1
            elif start_time in afternoon_time_slots and s.date.month == date.today().month:
                this_month_busiest_slots["Afternoon"] += 1
            elif start_time in evening_time_slots and s.date.month == date.today().month:
                this_month_busiest_slots["Evening"] += 1

        results["overall_busiest_slots"] = overall_busiest_slots
        results["this_month_busiest_slots"] = this_month_busiest_slots

        # Chart 4: Show gender distribution of patients
        patients_by_gender = {"Male": 0, "Female": 0, "Other": 0}
        for pID in patients_set:
            patient = db.get_or_404(Patient, pID)
            if patient.gender == "Male":
                patients_by_gender["Male"] += 1
            elif patient.gender == "Female":
                patients_by_gender["Female"] += 1
            else:
                patients_by_gender["Other"] += 1
        results["patients_by_gender"] = patients_by_gender

        return results, 200