from flask import Blueprint, redirect, url_for, request, jsonify
from .extensions import db
from .models import User
from .models import PlantEntry
from flask_cors import CORS
main = Blueprint('main', __name__)

@main.route('/')
def index():

    return f"<ul>{'funciona'}</ul>"

@main.route('/add', methods=['POST'])
def add():
    # Get data from the request
    data = request.get_json()  # Obtener el objeto JSON de la solicitud
    email = data['email']
    # occupation = data['occupation']
    occupation = 'test'
    password = data['password']
    # Check if user with the given email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email already in use"}), 400
    # If validation passes, add the user to the database
    user = User(email=email, password=password, occupation=occupation)
    db.session.add(user)
    db.session.commit()

    # # Return success response
    return jsonify({"message": "User added successfully"}), 201

@main.route('/userValidation', methods=['POST'])
def userValidation():
    # Get data from the request
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    # Check if user with the given email exists
    existing_user = User.query.filter_by(email=email).first()
        
    if not existing_user:
        return jsonify({"message": "User does not exist"}), 404

    # Check if the provided password matches the stored one
    if existing_user.password != password:
        return jsonify({"message": "Incorrect password"}), 401

    # If validation passes, return success response
    return jsonify({"message": "User validated successfully", "user": email}), 200


@main.route('/addPlant', methods=['POST'])
def add_plant():
    # Obtener el objeto JSON de la solicitud
    data = request.get_json()

    # Extraer los datos de la planta del JSON
    usuario = data['usuario']
    nombre = data['nombre']
    frecuenciaRiego = data['frecuenciaRiego']
    descripcion = data['descripcion']
    recomendaciones = data['recomendaciones']
    lastWateredTime = data['lastWateredTime']

    # Crear una nueva instancia de PlantEntry
    new_plant = PlantEntry(usuario=usuario, nombre=nombre, 
                           frecuenciaRiego=frecuenciaRiego, 
                           descripcion=descripcion, 
                           recomendaciones=recomendaciones,
                           lastWateredTime=lastWateredTime)

    # Agregar la nueva planta a la base de datos
    db.session.add(new_plant)

    # Intentar guardar en la base de datos y manejar posibles excepciones
    try:
        db.session.commit()
    except Exception as e:
        # Si hay un error, devolver un mensaje de error
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

    # Si todo es exitoso, devolver un mensaje de éxito
    return jsonify({"message": "Plant added successfully", "plant_id": new_plant.id}), 201

@main.route('/getUserPlants', methods=['GET'])
def get_user_plants():
    usuario = request.args.get('usuario')

    if not usuario:
        return jsonify({"message": "No user provided"}), 400

    try:
        # Buscar todas las plantas para el usuario dado
        plantas = PlantEntry.query.filter_by(usuario=usuario).all()
        plantas_data = [
            {
                "nombre": planta.nombre,
                "frecuenciaRiego": planta.frecuenciaRiego,
                "descripcion": planta.descripcion,
                "recomendaciones": planta.recomendaciones
            } for planta in plantas
        ]

        return jsonify(plantas_data), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

@main.route('/removePlant', methods=['POST'])
def remove_plant():
    # Extraer plant_id del cuerpo de la solicitud
    data = request.get_json()
    print(data)
    id = data.get('plantId')
    print(data)
    print(id)
    if not id:
        return jsonify({"message": "Plant ID is missing"}), 400

    # Buscar la entrada de planta por ID
    planta = PlantEntry.query.filter_by(id=id).first()
    print(planta)

    if planta is None:
        return jsonify({"message": "Plant not found"}), 404

    try:
        db.session.delete(planta)
        db.session.commit()
        return jsonify({"message": "Plant successfully deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500