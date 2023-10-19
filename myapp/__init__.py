import os
from flask import Flask 
from .extensions import db
from .routes import main
from .models import User
from flask_cors import CORS

def create_app():
    
    app = Flask(__name__)
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    # postgres://prettyprinted_render_example_user:11vq6k72GmFJazhVpz3pFUko50djVZT1@dpg-ceukdhmn6mpglqdb4avg-a.oregon-postgres.render.com/prettyprinted_render_example

    db.init_app(app)
    app.register_blueprint(main)

    # Check if the database needs to be initialized
    with app.app_context():
        db.drop_all()
        db.create_all()
        app.logger.info('Initialized the database!')
        
        new_user = User(email='diego@gmail.com', password='12345')
        db.session.add(new_user)
        db.session.commit()
    
    CORS(app, resources={r"/*": {"origins": "https://frontmastest.onrender.com"}})

        
    return app
