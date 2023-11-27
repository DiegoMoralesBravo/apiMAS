import os
import requests
import sys
import shutil
from flask import Flask 
from .extensions import db
from .routes import main
from .models import User
from flask_cors import CORS
# from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

def remove_files_in_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                # If you want to remove subdirectories as well, uncomment the following line
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

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

    sam_checkpoint = 'https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth'

    # # El nombre del archivo para guardar el modelo
    filename = sam_checkpoint.split('/')[-1]

    # file_path = model_path / filename
    checkpoint = os.path.join('/var/data', filename)

    with requests.get(sam_checkpoint, stream=True) as response:
        response.raise_for_status()
        with open(checkpoint, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192): 
                f.write(chunk)
    print("Descarga completada.")
    return app