from flask import Flask
from models import *
from flask_migrate import Migrate

migrate = Migrate()

def create_app():
    app = Flask(__name__,static_folder="static",static_url_path="/static")
    app.secret_key = "12345"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["UPLOAD_PP"] = "static/uploads/profile_pics" 
    app.config["UPLOAD_RESUME"] = "static/uploads/resumes"


    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'openmaterial01@gmail.com'
    app.config['MAIL_PASSWORD'] = 'your_password'
    app.config['MAIL_DEFAULT_SENDER'] = 'openmaterial01@gmail.com'

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    return app
