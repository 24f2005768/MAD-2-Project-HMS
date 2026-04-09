from app import app 
from models import db, Admin
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_security.utils import hash_password 

# run this file with this command from the backend folder: python3 -m scripts.init_db

with app.app_context():
    db.drop_all()
    db.create_all()
    datastore: SQLAlchemyUserDatastore = app.datastore

    # creating roles
    admin_role = datastore.find_or_create_role('Admin')
    doctor_role = datastore.find_or_create_role('Doctor')
    patient_role = datastore.find_or_create_role('Patient')

    # creating admin 
    if not datastore.find_user(user_name = 'Admin',):
        user = datastore.create_user(
            user_name = 'Admin',
            user_password = hash_password('123456'),
            contact_number = '0123456789',
            email = 'admin@gmail.com'
        )

    db.session.add(user)
    user.user_admin = Admin(name = 'Kriti')

    admin = datastore.find_user(user_name = 'Admin')
    admin_role = datastore.find_role('Admin')

    datastore.add_role_to_user(admin, admin_role)

    from models import *
    from model_code import create_initial_data
    create_initial_data()


    db.session.commit()