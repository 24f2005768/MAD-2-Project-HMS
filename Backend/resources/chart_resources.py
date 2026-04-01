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