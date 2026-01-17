from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from resources import auth_blueprint, api, api_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_database.sqlite3'
app.secret_key = 'secret'
app.config['SECURITY_PASSWORD_SALT'] = 'secret_salt'
app.config['SECURITY_PASSWORD_HASH'] = 'argon2'

app.app_context().push()

from models import db, User, Role
db.init_app(app)

from flask_security.datastore import SQLAlchemyUserDatastore
from extensions import security 

datastore = SQLAlchemyUserDatastore(db, User, Role)
security.init_app(app, datastore = datastore)

app.datastore = datastore

app.register_blueprint(auth_blueprint)
app.register_blueprint(api_bp)


@app.route('/')
def home():
    return 'hello'

if __name__ == '__main__':
    app.run(debug = True)