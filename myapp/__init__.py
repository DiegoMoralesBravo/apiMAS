import os

from flask import Flask 
import SQLAlchemy as sa
from .extensions import db
from .routes import main

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    # postgres://prettyprinted_render_example_user:11vq6k72GmFJazhVpz3pFUko50djVZT1@dpg-ceukdhmn6mpglqdb4avg-a.oregon-postgres.render.com/prettyprinted_render_example

    db.init_app(app)

    app.register_blueprint(main)

    # Check if the database needs to be initialized
    with app.app_context():
        db.drop_all()
        db.create_all()
        app.logger.info('Initialized the database!')


    return app


    return app