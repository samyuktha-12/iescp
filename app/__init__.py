from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
csrf = CSRFProtect(app) 
CORS(app)

from app import routes, models, resources

