from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

from config.environment import db_URI

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = db_URI

db = SQLAlchemy(app)
marsh = Marshmallow(app)
bcrypt = Bcrypt(app)

from models import user, userType, classes, classAttendee, classType
from controllers.users import users_controller
from controllers.classController import classes_controller
from controllers.classType import class_type_controller


app.register_blueprint(users_controller, url_prefix="/api")
app.register_blueprint(classes_controller, url_prefix="/api")
app.register_blueprint(class_type_controller, url_prefix="/api")
