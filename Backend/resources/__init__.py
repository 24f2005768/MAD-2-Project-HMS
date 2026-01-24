from flask import Blueprint
from flask_restful import Api

from resources.auth_resources import auth_blueprint, LoginResource, RegisterResource, LogoutResource
from resources.doctor_resources import DoctorResources, AllDoctorResources
from resources.patient_resources import PatientResources, AllPatientResources

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(LoginResource, "/login")
api.add_resource(LogoutResource, "/logout")

# Doctor Routes
api.add_resource(DoctorResources, "/doctor", "/doctor/<int:doctor_id>")
api.add_resource(AllDoctorResources, "/doctors")

# Patient Routes
api.add_resource(RegisterResource, "/register")
api.add_resource(PatientResources, "/patient", "/patient/<int:patient_id>")
api.add_resource(AllPatientResources, "/patients")