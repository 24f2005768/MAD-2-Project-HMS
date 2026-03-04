from app import *
from models import *
from datetime import time, date, timedelta
from sqlalchemy import or_, desc, asc

# dates = Shift.query.order_by(desc(Shift.id)).all()
# search_query = "23"

patient = db.get_or_404(Patient, 1)
print(patient.get_age())
# doctor_shift = doctor.doctor_shift


