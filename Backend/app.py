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
from model_code import add_upcoming_appt
add_upcoming_appt()

#----------------------------------------------Run the app---------------------------------------------------
if __name__ == '__main__':
    app.run(debug = True)
