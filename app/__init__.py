from app import config
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import datetime

application = Flask(__name__)
application.config.from_object(config.Config)

db = SQLAlchemy(application)

@application.before_request
def make_session_permanent():
    session.permanent = True
    application.permanent_session_lifetime = datetime.timedelta(days=30)

from app import models
from app import functions
from app import routes