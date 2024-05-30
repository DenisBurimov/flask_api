import os
from flask import Flask
from flask_migrate import Migrate
from .database import db

migration = Migrate()

def create_app(environment="development"):
    from config import config
    from app import models as m
    from .views import product_blueprint
    
    app = Flask(__name__)
    
    env = os.environ.get("APP_ENV", environment)
    configuration = config(env)
    app.config.from_object(configuration)
    configuration.configure(app)

    # Set up extensions.
    db.init_app(app)
    migration.init_app(app, db)
    
    app.register_blueprint(product_blueprint)
    
    return app
