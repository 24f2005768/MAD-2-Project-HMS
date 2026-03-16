from models import *

def mark_past_appointments_completed():
    past_apt = Appointment.query.filter(Appointment.date < date.today(), Appointment.status == "Booked").all()
    for a in past_apt:
        a.app_t = Treatment(diagnosis='Some diagnosis from doctor', notes = 'Some notes from doctor', prescription = 'Some prescription from doctor', tests = 'Some tests from doctor')
        a.status = "Completed"
        db.session.commit()
    return True
