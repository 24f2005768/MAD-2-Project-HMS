from flask_security.core import UserMixin, RoleMixin
from extensions import db
from datetime import datetime, timedelta, date

# relationships

# One-to-One:
# One-to-Many: 
# Many-to-Many: User-Role

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_name = db.Column(db.String(32), nullable = False, unique = True)
    user_password = db.Column(db.String(32), nullable = False)
    
    # for flask-security-too
    roles = db.relationship('Role', backref = 'users', secondary = 'user_role')
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False)
    active = db.Column(db.Boolean, default = True) # if Active = False, then the user will not be able to login

    admin_user = db.relationship('Admin', back_populates = 'a', uselist = False)
    doctor_user = db.relationship('Doctor', back_populates = 'd', uselist = False)
    patient_user = db.relationship('Patient', back_populates = 'p', uselist = False)

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    users = db.relationship('User', back_populates = 'roles', secondary = 'user_role')

class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    contact_number = db.Column(db.String, nullable = False)

    admin_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    a = db.relationship('User', back_populates = 'admin_relationship')
    
class Department(db.Model):
    __tablename__ = 'department'
    department_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String, default = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum')
    status = db.Column(db.String) # DeletedbyAdmin

    department_profile_picture = db.Column(db.Integer, db.ForeignKey('profile_pictures.name'))
    
    doctors = db.relationship('Doctor', back_populates = 'dept')
    department_pfp = db.relationship('ProfilePictures', back_populates = 'pfp_department')

class Doctor(db.Model):
    __tablename__ = 'doctor'
    doctor_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(64), nullable = False)
    contact_number = db.Column(db.String, nullable = False)
    email = db.Column(db.String)
    dob = db.Column(db.Date, nullable = False)
    blacklisted = db.Column(db.Boolean, default = False)
    description = db.Column(db.String, default = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum')
    gender = db.Column(db.String)
    status = db.Column(db.String) # DeletedbyAdmin

    # doctor_profile_picture = db.Column(db.String, db.ForeignKey('profile_pictures.name'))
    department_id = db.Column(db.Integer, db.ForeignKey(Department.department_id))
    doctor_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    dept = db.relationship('Department', back_populates = 'doctors')
    d = db.relationship('User', back_populates = 'doctor_relationship')
    appointment_d = db.relationship('Appointment', back_populates = 'd_ref')
    doctor_slot = db.relationship('SlotSchedules', back_populates = 'slot_doctor')
    doctor_notif = db.relationship('AvailabilityNotifications', back_populates = 'notif_doctor')
    # doctor_pfp = db.relationship('ProfilePictures', back_populates = 'pfp_doctor')

class Patient(db.Model):
    __tablename__ = 'patient'
    patient_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(64), nullable = False)
    contact_number = db.Column(db.String(10), nullable = False)
    gender = db.Column(db.String)
    email = db.Column(db.String)
    dob = db.Column(db.Date, nullable = False)
    blacklisted = db.Column(db.Boolean, default = False)
    age = db.Column(db.Integer)
    height = db.Column(db.String, default = '--')
    weight = db.Column(db.String, default = '--')
    status = db.Column(db.String) # DeletedbyAdmin

    # patient_profile_picture = db.Column(db.String, db.ForeignKey('profile_pictures.name'))
    patient_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    p = db.relationship('User', back_populates = 'patient_relationship')
    appointment_p = db.relationship('Appointment', back_populates = 'p_ref', uselist = False)
    patient_slot = db.relationship('SlotSchedules', back_populates = 'slot_patient')
    patient_notif = db.relationship('AvailabilityNotifications', back_populates = 'notif_patient')
    # patient_pfp = db.relationship('ProfilePictures', back_populates = 'pfp_patient')

# class Appointment(db.Model):
#     __tablename__ = 'appointment'
#     appointment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     date_time = db.Column(db.Date, nullable = False, default = datetime.now)

#     t_id = db.Column(db.Integer, db.ForeignKey('treatment.treatment_id'))
#     doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'))
#     patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
#     s_sch_id = db.Column(db.Integer, db.ForeignKey('slot_schedules.schedule_id'))

#     d_ref = db.relationship('Doctor', back_populates = 'appointment_d')
#     p_ref = db.relationship('Patient', back_populates = 'appointment_p')
#     t = db.relationship('Treatment', back_populates = 'ap', uselist = False)
#     appointment_sch = db.relationship('SlotSchedules', back_populates = 'slot_sch_appointment_rel')

# class Treatment(db.Model):
#     __tablename__ = 'treatment'
#     treatment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     status = db.Column(db.String)
#     diagnosis = db.Column(db.String) 
#     prescription = db.Column(db.String)
#     notes = db.Column(db.String)    
#     tests = db.Column(db.String)
#     diet_type = db.Column(db.String)

#     ap = db.relationship('Appointment', back_populates = 't')
#     treatment_dn = db.relationship('DieticianNotes', back_populates = 'dn_treatment', uselist = False)

# class Slot(db.Model):
#     __tablename__ = 'slot'
#     slot_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     name = db.Column(db.String)
#     time = db.Column(db.String)

#     s_schedule = db.relationship('SlotSchedules', back_populates = 's_sch')

# class SlotSchedules(db.Model):
    __tablename__ = 'slot_schedules'
    schedule_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    date = db.Column(db.Date, default = datetime.now)

    slot_doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'))
    slot_patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    schedule_slot_id = db.Column(db.Integer, db.ForeignKey('slot.slot_id'))

    slot_doctor = db.relationship('Doctor', back_populates = 'doctor_slot')
    slot_patient = db.relationship('Patient', back_populates = 'patient_slot')
    s_sch = db.relationship('Slot', back_populates = 's_schedule')
    slot_sch_appointment_rel = db.relationship('Appointment', back_populates = 'appointment_sch', uselist = False)
