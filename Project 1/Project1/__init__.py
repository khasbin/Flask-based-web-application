from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME  = "databadse.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']  = "hakdhkagladkfgadkkadgfladsjgkfd3242526@#$%@adfad"
    app.config['SQLALCHEMY_DATABASE_URI']= f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .models import Note, User

    create_database(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app


def create_database(app):
    if not(os.path.exists('project1/' +DB_NAME)):
        db.create_all(app = app)
        print('Created Database')

 

