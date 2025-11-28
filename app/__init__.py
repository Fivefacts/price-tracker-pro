from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pricetracker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    from .models import db
    db.init_app(app)
    
    with app.app_context():
        from . import app as app_module
        db.create_all()
    
    return app