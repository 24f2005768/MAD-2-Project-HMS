from flask import Blueprint
from flask_restful import Api

from resources.auth_resources import LoginResource, RegisterResource, LogoutResource
from resources.doctor_resources import DoctorResources, AllDoctorResources, Availability, DoctorAppointments
from resources.patient_resources import PatientResources, AllPatientResources, PatientTreatmentHistory
from resources.appointment_resources import AppointmentResources, AllAppointmentResources, SelectShift, BookAppointment, CancelAppointment, RescheduleAppointment, TreatmentResources
from resources.department_resources import DepartmentResources, AllDepartmentResources
from resources.search_resources import AdminSearch, DoctorSearch, PatientSearch
from resources.chart_resources import AdminChartsResources, PatientChartsResources

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(LoginResource, "/login")
api.add_resource(LogoutResource, "/logout")

# Doctor Routes
api.add_resource(DoctorResources, "/doctor", "/doctor/<int:doctor_id>")
api.add_resource(AllDoctorResources, "/doctors")
api.add_resource(Availability, "/doctor/availability/<int:doctor_id>")
api.add_resource(DoctorAppointments, "/doctor/appointments/<int:doctor_id>")

# Department Routes
api.add_resource(DepartmentResources, "/dept", "/dept/<int:dept_id>")
api.add_resource(AllDepartmentResources, "/depts")

# Patient Routes
api.add_resource(RegisterResource, "/register")
api.add_resource(PatientResources, "/patient", "/patient/<int:patient_id>")
api.add_resource(AllPatientResources, "/patients")
api.add_resource(PatientTreatmentHistory, "/patient/treatment-history/<int:patient_id>")

# Appointment Routes
api.add_resource(AppointmentResources, '/appointment', '/appointment/<int:appointment_id>')
api.add_resource(AllAppointmentResources, '/appointments')
api.add_resource(SelectShift, '/select-shift/<int:doctor_id>/<int:shift_id>')
api.add_resource(BookAppointment, '/book-appointment/<int:slot_id>')
api.add_resource(CancelAppointment, '/cancel-appointment/<int:appointment_id>')
api.add_resource(RescheduleAppointment, '/reschedule-appointment/<int:appointment_id>')
api.add_resource(TreatmentResources, '/treatment/<int:id>')

# Search Routes
api.add_resource(AdminSearch, "/admin/search")
api.add_resource(DoctorSearch, "/doctor/search")
api.add_resource(PatientSearch, "/patient/search")

# Chart Routes 
api.add_resource(AdminChartsResources, "/admin/charts")
api.add_resource(PatientChartsResources, "/patient/charts/<int:patient_id>")