from flask_security.core import UserMixin, RoleMixin
from extensions import db
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

# relationships

# One-to-One: Appointment-Treatment
# One-to-Many: 
# Many-to-Many: User-Role

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_name = db.Column(db.String(32), nullable = False, unique = True)
    user_password = db.Column(db.String, nullable = False)
    contact_number = db.Column(db.String)
    email = db.Column(db.String)
    blacklisted = db.Column(db.Boolean, default = False) 
    
    # for flask-security-too
    roles = db.relationship('Role', back_populates = 'users', secondary = 'user_role')
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False)
    active = db.Column(db.Boolean, default = True) # if Active = False, then the user will not be able to login

    user_admin = db.relationship('Admin', back_populates = 'admin_user', uselist = False)
    user_doctor = db.relationship('Doctor', back_populates = 'doctor_user', uselist = False)
    user_patient = db.relationship('Patient', back_populates = 'patient_user', uselist = False)

    def role(self):
        return self.roles[0].name

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)

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

    admin_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    admin_user = db.relationship('User', back_populates = 'user_admin')

class Patient(db.Model):
    __tablename__ = 'patient'
    patient_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(64), nullable = False)
    dob = db.Column(db.Date)
    gender = db.Column(db.String)
    height = db.Column(db.String, default = '--')
    weight = db.Column(db.String, default = '--')
    status = db.Column(db.String) # DeletedbyAdmin

    pfp = db.Column(db.String, db.ForeignKey('profile_pictures.name'))
    patient_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    patient_user = db.relationship('User', back_populates = 'user_patient')

    # oneToMany relationship with Slots
    patient_slots = db.relationship('Slots', back_populates = 'slots_patient')
    patient_app = db.relationship('Appointment', back_populates = 'app_patient', uselist = False)
    patient_pfp = db.relationship('ProfilePictures', back_populates = 'pfp_patient')

    def get_age(self):
        dob = self.dob
        age = relativedelta(date.today(), dob)
        res = f"{age.years} years, {age.months} months, {age.days} days"
        return res
    
    def get_age_in_years(self):
        dob = self.dob
        age = relativedelta(date.today(), dob)
        return age.years
    
class Department(db.Model):
    __tablename__ = 'department'
    department_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String, default = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum')
    status = db.Column(db.String) # DeletedbyAdmin

    pfp = db.Column(db.String, db.ForeignKey('profile_pictures.name'), default = "DefaultDepartment")

    # oneToMany relationship with Doctor
    doctors = db.relationship('Doctor', back_populates = 'dept')
    department_pfp = db.relationship('ProfilePictures', back_populates = 'pfp_department')

# association table for Doctor and Shift
doctor_availability = db.Table('doctor_availability',
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.doctor_id')),
    db.Column('shift_id', db.Integer, db.ForeignKey('shift.id'))
)

class Doctor(db.Model):
    __tablename__ = 'doctor'
    doctor_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(64), nullable = False)
    dob = db.Column(db.Date)
    description = db.Column(db.String, default = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum')
    gender = db.Column(db.String)
    status = db.Column(db.String) # DeletedbyAdmin

    pfp = db.Column(db.String, db.ForeignKey('profile_pictures.name'))
    department_id = db.Column(db.Integer, db.ForeignKey(Department.department_id))
    doctor_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    doctor_user = db.relationship('User', back_populates = 'user_doctor')
    # Many doctors can have one department
    dept = db.relationship('Department', back_populates = 'doctors')
    # manyToMany relationship with Shift
    doctor_shift = db.relationship('Shift', secondary = doctor_availability, back_populates = 'shift_doctor')
    # oneToMany relationship with Slots
    doctor_slots = db.relationship('Slots', back_populates = 'slots_doctor')
    doctor_app = db.relationship('Appointment', back_populates = 'app_doctor')
    doctor_pfp = db.relationship('ProfilePictures', back_populates = 'pfp_doctor')

# table to store 'shift'-wise data for doctors, automatic addition of dates and shifts when app is initialized
class Shift(db.Model):
    __tablename__ = 'shift'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    # date is DateTime so we can break it into 15 minutes slots with that date and time
    date = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    # manyToMany relationship with Doctor
    shift_doctor = db.relationship('Doctor', secondary = doctor_availability, back_populates = 'doctor_shift')
    shifts_slots = db.relationship('Slots', back_populates = 'slots_shifts')
    
# Main table to store appointments of patients
class Appointment(db.Model):
    __tablename__ = 'appointment'
    appointment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    date = db.Column(db.Date, nullable = False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    status = db.Column(db.String)

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    slot_id = db.Column(db.Integer, db.ForeignKey('slots.id'))

    app_doctor = db.relationship('Doctor', back_populates = 'doctor_app')
    app_patient = db.relationship('Patient', back_populates = 'patient_app')
    app_t = db.relationship('Treatment', back_populates = 't_app', uselist = False)
    app_slots = db.relationship('Slots', back_populates = 'slots_app')

class Treatment(db.Model):
    __tablename__ = 'treatment'
    treatment_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    diagnosis = db.Column(db.String) 
    notes = db.Column(db.String)    
    prescription = db.Column(db.String)
    tests = db.Column(db.String)

    appt_id = db.Column(db.Integer, db.ForeignKey('appointment.appointment_id'))

    t_app = db.relationship('Appointment', back_populates = 'app_t')

# temporary table to store 15-15 minutes sessions for doctors and patients
# rows are added when a doctor provide shift and date, shift is broken into 15-15 minutes slots 
class Slots(db.Model):
    __tablename__ = 'slots'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    date = db.Column(db.Date)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'))
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'))

    # One (patient or doctor) can have multiple entries
    slots_doctor = db.relationship('Doctor', back_populates = 'doctor_slots')
    slots_patient = db.relationship('Patient', back_populates = 'patient_slots')
    slots_app = db.relationship('Appointment', back_populates = 'app_slots', uselist = False)
    slots_shifts = db.relationship('Shift', back_populates = 'shifts_slots')

class ProfilePictures(db.Model):
    __tablename__ = 'profile_pictures'
    picture_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    role = db.Column(db.String)

    pfp_doctor = db.relationship('Doctor', back_populates = 'doctor_pfp')
    pfp_patient = db.relationship('Patient', back_populates = 'patient_pfp')
    pfp_department = db.relationship('Department', back_populates = 'department_pfp')
