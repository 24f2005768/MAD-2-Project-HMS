from celery import shared_task
from datetime import date, timedelta, time, datetime
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from pathlib import Path
import csv
from reminders import send_email

# Add Backend to path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from models import *
from app import *

SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "k@email.com"

def monthly_report_patients():
    date_today = date.today()
    patients = Patient.query.all()

    reports_folder = Path(__file__).parent.parent / "reports"  # Backend/reports
    
    for patient in patients:
        filename = reports_folder/ f"{patient.name}_monthly_report_{date_today.year}_{date_today.month}.csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)    

            # header 
            writer.writerow(["Date", "Doctor", "Department", "Start Time", "End Time", "Status"])

            start_d = datetime.datetime(year = date_today.year, month=date_today.month, day = 1)
            monthly_appointments = Appointment.query.filter(Appointment.start_time >= start_d, Appointment.patient_id == patient.patient_id).all()

            for appt in monthly_appointments:
                writer.writerow([appt.date, 
                                 appt.app_doctor.name,
                                 appt.app_doctor.dept.name,
                                 appt.start_time,
                                 appt.end_time,
                                 appt.status])
                
        send_email(
                patient.patient_user.email,
                f"Monthly Report - {date_today.strftime('%B %Y')}",
                f"""Dear {patient.name},
                    <br><br>Please find your monthly report attached.
                    <br><br>Thank you,<br>LDH Hospital""",
                filename
            ) 

    return filename

# send_email("a@gmail.com", subject = "Test Mail 2", message = message)
monthly_report_patients()