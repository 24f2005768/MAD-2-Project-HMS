from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from resources import api_bp
from flask_cors import CORS
from flask_caching import Cache
from celery import Celery, Task
from celery.schedules import crontab

from tasks import reminders
from caching_config import cache

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_database.sqlite3'
app.secret_key = 'secret'
app.config['SECURITY_PASSWORD_SALT'] = 'secret_salt'
app.config['SECURITY_PASSWORD_HASH'] = 'argon2'

# flask caching
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 60
cache.init_app(app)

# ---------------------------------------------------------------- celery -------------------------------------------------------------------

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask, broker="redis://localhost:6379/0", backend="redis://localhost:6379/1")
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

app.config.from_mapping(
    CELERY=dict(
        timezone = 'Asia/Kolkata',
    ),
)
celery_app = celery_init_app(app)

# Periodic Tasks
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    # Executes every day morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=19, minute=16),
        reminders.patient_daily_reminders.s(),
        name="daily-reminders"
    )

    # Executes monthly report on the 1st of each month at 9 AM
    # sender.add_periodic_task(
    #     crontab(day_of_month=1, hour=9, minute=0),
    #     reminders.monthly_report_doctors.s(),
    #     name="monthly-report"
    # )
# ---------------------------------------------------------------------------------------------------------------------------------------------------

app.app_context().push()

from models import db, User, Role
db.init_app(app)

# for flask API
CORS(app, origins=['http://localhost:5173'])

from flask_security.datastore import SQLAlchemyUserDatastore
from extensions import security 

# for flask security
datastore = SQLAlchemyUserDatastore(db, User, Role)
security.init_app(app, datastore = datastore)

app.datastore = datastore

# registering blueprint
app.register_blueprint(api_bp)

#-------------------------------------------- For model code-----------------------------------------------

# check if any date in the coming week is missing
# if any date is missing, add rows to the shift table

from upcoming_week import add_missing_shifts
add_missing_shifts()

# check if there are any past appointments which are not marked as completed

from mark_past_appointments import mark_past_appointments_completed
mark_past_appointments_completed()

# add upcoming doctor slots and appointments

from models import *
from upcoming_appt import add_doctor_shifts_today, add_doctor_shifts_tomorrow, add_doctor_shifts_day_after_tomorrow

date_today = date.today()
time = datetime.min.time()
date_today = datetime.combine(date_today, time)
next_week_dates = [(date_today + timedelta(days = i)) for i in range(1,8)]

check_slots_for_today = Shift.query.filter(Shift.date == date_today).first()
check_slots_for_tomorrow = Shift.query.filter(Shift.date == next_week_dates[0]).first()
check_slots_for_day_after_tomorrow = Shift.query.filter(Shift.date == next_week_dates[1]).first()

add_availability_appointments_today = check_slots_for_today.shift_doctor
add_availability_appointments_tomorrow = check_slots_for_tomorrow.shift_doctor
add_availability_appointments_day_after_tomorrow = check_slots_for_day_after_tomorrow.shift_doctor
if add_availability_appointments_today == []:
    add_doctor_shifts_today()

if add_availability_appointments_tomorrow == []:
    add_doctor_shifts_tomorrow()

if add_availability_appointments_day_after_tomorrow == []:
    add_doctor_shifts_day_after_tomorrow()

#----------------------------------------------Run the app---------------------------------------------------
if __name__ == '__main__':
    app.run(debug = True)