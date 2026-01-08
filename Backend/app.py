from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_database.sqlite3'
app.secret_key = 'secret'

app.app_context().push()
db = SQLAlchemy()
db.init_app(app)

from models import *

@app.route('/')
def home():
    return 'hello'

if __name__ == '__main__':
    app.run(debug = True)