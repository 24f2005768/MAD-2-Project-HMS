# Add Backend to path
from pathlib import Path
import sys 

backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))
from models import *

from celery import shared_task
from datetime import date, timedelta, time, datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template
from pathlib import Path
import csv

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "k@email.com"

def send_email(to_address, subject, message, attachment = None):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))

    if attachment:
        reports_folder = Path(__file__).parent.parent / "reports" 
        with open(reports_folder/attachment, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={attachment}")
            msg.attach(part)

    server = smtplib.SMTP(host = SMTP_SERVER_HOST, port = SMTP_SERVER_PORT)
    server.send_message(msg)
    server.quit()

    return True

# Celery task to send daily reminders to patients
@shared_task()
def patient_daily_reminders():
    now = datetime.now()
    today_appt = Appointment.query.filter(Appointment.date == date.today(), Appointment.status == "Booked").all()
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

    # Get the path to patient_daily_reminders.html
    script_dir = Path(__file__).parent
    template_path = script_dir / "patient_daily_reminders.html"

    with open(template_path) as file:
        template = Template(file.read())

    for p_ID in patients_dict:
        patient = db.get_or_404(Patient, p_ID)
        reminder_message = patients_dict[p_ID]["message"]
        appt = patients_dict[p_ID]["appointments"]
        message = template.render(appt = appt, patient = patient, reminder_message = reminder_message, now = now)
        send_email(patient.patient_user.email, "Appointment reminder", message = message)

@shared_task
def treatment_history_patient(patient_id):
    now = datetime.now()
    patient = Patient.query.filter(Patient.patient_id == patient_id).first()

    reports_folder = Path(__file__).parent.parent / "reports"  # Backend/reports
    
    filename = f"{patient.name}_treatment_history.csv"
    with open(reports_folder/filename, "w", newline="") as file:
        writer = csv.writer(file)    

        # header 
        writer.writerow(["Date", "Doctor", "Department", "Start Time", "End Time", "Status", "Diagnosis", "Notes", "Prescription", "Tests"])

        appointments = Appointment.query.filter(Appointment.patient_id == patient.patient_id).all()

        for appt in appointments:
            if appt.status == "Completed":
                writer.writerow([appt.date, 
                                    appt.app_doctor.name,
                                    appt.app_doctor.dept.name,
                                    appt.start_time,
                                    appt.end_time,
                                    appt.status,
                                    appt.app_t.diagnosis,
                                    appt.app_t.notes,
                                    appt.app_t.prescription,
                                    appt.app_t.notes])
            else:
                writer.writerow([appt.date, 
                                    appt.app_doctor.name,
                                    appt.app_doctor.dept.name,
                                    appt.start_time,
                                    appt.end_time,
                                    appt.status,
                                    "--",
                                    "--",
                                    "--",
                                    "--"])

    # Path to treatment_history.html
    script_dir = Path(__file__).parent
    template_path = script_dir / "treatment_history.html"

    with open(template_path) as t:
        template = Template(t.read())    
    
    message = template.render(patient = patient, now = now)
    send_email(
            patient.patient_user.email, "Treatment History Report", message, filename) 

    return filename

@shared_task()
def monthly_report_doctor(doctor_id):
    now = datetime.now()

    doctor = db.get_or_404(Doctor, doctor_id)
    prev_month_dates = [(date.today() + timedelta(days = -i)) for i in range(1, 32)]
    prev_month_appts = []
    for d in prev_month_dates:
        prev_month_appts += Appointment.query.filter(Appointment.date == d, Appointment.doctor_id == doctor.doctor_id).all()

    # Get the path to monthly_report.html
    script_dir = Path(__file__).parent
    template_path = script_dir / "monthly_report.html"

    with open(template_path) as file:
        template = Template(file.read())

    report_message = f"Hi {doctor.name}, here is your monthly report for {datetime.strftime(now, "%B")}"
    message = template.render(appt = prev_month_appts, doctor = doctor, report_message = report_message, now = now)
    send_email(doctor.doctor_user.email, f"Monthly Report {datetime.strftime(now, "%B")}", message = message)

