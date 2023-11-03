import os
from flask import Flask 
from .extensions import db
from .routes import main
from .models import User
from flask_cors import CORS
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor


def create_app():
    
    app = Flask(__name__)

    # CORS setup
    CORS(app, resources={r"/*": {"origins": "https://frontmastest.onrender.com"}})

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    db.init_app(app)
    app.register_blueprint(main)

    # Check if the database needs to be initialized
    with app.app_context():
        db.drop_all()
        db.create_all()
        app.logger.info('Initialized the database!')
        
        # Consider removing hardcoded user or ensuring it's only for testing
        new_user = User(email='diego@gmail.com', password='12345', occupation='student')
        db.session.add(new_user)
        db.session.commit()
        
    
    model_type = "vit_h"

    device = "cuda"
    
    sam_checkpoint = './https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth'


    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)

    mask_generator = SamAutomaticMaskGenerator(sam)   
     
    return app