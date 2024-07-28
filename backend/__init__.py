from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from celery import Celery, Task
import os

current_directory = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_PASSWORD_SALT'] = 'saltsecurity'
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
app.config['SEND_WILDCARD'] = True


db = SQLAlchemy(app)
api = Api(app, prefix='/api')
jwt = JWTManager(app)
with app.app_context():
    from backend.api import initialize_api
    from backend.models import User
    initialize_api()


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object('config')
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

celery_app = celery_init_app(app)


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