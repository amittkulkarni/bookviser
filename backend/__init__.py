from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from backend.celeryapp import celery_init_app
import os


current_directory = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['WTF_CSRF_ENABLED'] = False
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_WILDCARD'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'd69f5b595ee070'
app.config['MAIL_PASSWORD'] = 'a2c01223352d98'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


db = SQLAlchemy(app)
api = Api(app, prefix='/api')
jwt = JWTManager(app)
celery_app = celery_init_app(app)
mail = Mail(app)
with app.app_context():
    from backend.api import initialize_api
    from backend.models import User
    initialize_api()


def create_tables():
    db.create_all()
    if not User.query.filter_by(username='librarian').first():
        admin_user = User(
            username='librarian',
            email='librarian@email.com',
            password='librarian_password',
            role='librarian'
        )
        db.session.add(admin_user)
        db.session.commit()


from backend.api import resources
