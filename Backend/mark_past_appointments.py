from models import *

def mark_past_appointments_completed():
    past_apt = Appointment.query.filter(Appointment.date < date.today(), Appointment.status == "Booked").all()
    for a in past_apt:
        a.status = 'Completed'
        a.app_t.diagnosis='Some diagnosis from doctor'
        a.app_t.notes = 'Some notes from doctor'
        a.app_t.prescription = 'Some prescription from doctor'
        a.app_t.tests = 'Some tests from doctor'
        db.session.commit()
    return True