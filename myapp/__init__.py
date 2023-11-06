import os
import requests
from flask import Flask 
from .extensions import db
from .routes import main
from .models import User
from flask_cors import CORS
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
from pathlib import Path

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

    device = "cpu"
    sam_checkpoint = 'https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth'

    # El directorio donde quieres guardar el modelo
    model_directory = '/var/data/sam_checkpoint/'
    model_path = Path(model_directory)

    # Crea el directorio si no existe
    model_path.mkdir(parents=True, exist_ok=True)

    # El nombre del archivo para guardar el modelo
    filename = sam_checkpoint.split('/')[-1]
    file_path = model_path / filename

    # Descarga el archivo solo si no existe
    if not file_path.exists():
        print(f"Descargando el modelo preentrenado a {file_path}...")
        response = requests.get(sam_checkpoint)
        response.raise_for_status()  # Verificar que la descarga fue exitosa
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print("Descarga completada.")
    else:
        print(f"El modelo ya está descargado en {file_path}.")

    # Ahora, puedes cargar el modelo utilizando la ruta del archivo descargado
    sam_checkpoint = str(file_path)

    # Código para inicializar y utilizar tu modelo
    # Suponiendo que 'sam_model_registry' y 'SamAutomaticMaskGenerator' ya están definidos e importados correctamente
    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)
    mask_generator = SamAutomaticMaskGenerator(sam)  
     
    return app