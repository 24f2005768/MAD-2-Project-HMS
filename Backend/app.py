from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from resources import api_bp
from flask_cors import CORS
from flask_caching import Cache
from celery import Celery, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_database.sqlite3'
app.secret_key = 'secret'
app.config['SECURITY_PASSWORD_SALT'] = 'secret_salt'
app.config['SECURITY_PASSWORD_HASH'] = 'argon2'

# flask caching
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300
cache = Cache(app)

# testing cache

from datetime import timezone
import datetime

@app.route('/cache')
@cache.cached()
def cache():
    return {"date" : str(datetime.datetime.now(timezone.utc))}

# celery

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost:6379/0",
        result_backend="redis://localhost:6379/1",
        timezone = 'Asia/Kolkata',
    ),
)
celery_app = celery_init_app(app)

# testing celery

from tasks.test import add

@app.route("/celery-task")
def task():
    add.delay(1,2)
    return {"message": "task started"}

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

# check if any date in the coming week is missing
# if any date is missing, add rows to the shift table

from upcoming_week import add_missing_shifts
add_missing_shifts()

# check if there are any past appointments which are not marked as completed

from mark_past_appointments import mark_past_appointments_completed
mark_past_appointments_completed()

if __name__ == '__main__':
    app.run(debug = True)