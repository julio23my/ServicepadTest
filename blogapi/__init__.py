import os
from flask import Flask
from blogapi.extensions import db, migrate
from blogapi.routes.users import user
from blogapi.routes.posts import post
from blogapi.routes.errors import error

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
    
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(error)
    app.register_blueprint(user)
    app.register_blueprint(post)
    
    return app