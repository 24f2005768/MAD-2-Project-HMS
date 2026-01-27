from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from resources import api, api_bp
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_database.sqlite3'
app.secret_key = 'secret'
app.config['SECURITY_PASSWORD_SALT'] = 'secret_salt'
app.config['SECURITY_PASSWORD_HASH'] = 'argon2'

app.app_context().push()

from models import db, User, Role
db.init_app(app)

CORS(app, origins=['http://localhost:5173'])

from flask_security.datastore import SQLAlchemyUserDatastore
from extensions import security 

datastore = SQLAlchemyUserDatastore(db, User, Role)
security.init_app(app, datastore = datastore)

app.datastore = datastore

app.register_blueprint(api_bp)


@app.route('/')
def home():
    return 'hello'

if __name__ == '__main__':
    app.run(debug = True)