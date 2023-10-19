from flask import Blueprint, redirect, url_for, request, jsonify
from .extensions import db
from .models import User
from flask_cors import CORS

main = Blueprint('main', __name__)

@main.route('/')
def index():
    users = User.query.all()
    users_list_html = [f"<li>{ user.email }</li>" for user in users]
    return f"<ul>{''.join(users_list_html)}</ul>"

@main.route('/add', methods=['POST'])
def add_user():
    # Get data from the request
    data = request.json
    email = data.get('email')
    occupation = data.get('occupation')
    password = data.get('password')

    # Check if user with the given email already exists
    existing_user = User.query.filter_by(username=email).first()
    if existing_user:
        return jsonify({"message": "Email already in use"}), 400

    # If validation passes, add the user to the database
    user = User(username=email, password=password, occupation=occupation)
    db.session.add(user)
    db.session.commit()

    # Return success response
    return jsonify({"message": "User added successfully"}), 201

from werkzeug.security import check_password_hash
from flask import request, jsonify

@main.route('/userValidation', methods=['POST'])
def userValidation():
    # Get data from the request
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Check if user with the given email exists
    existing_user = User.query.filter_by(username=email).first()
    
    if not existing_user:
        return jsonify({"message": "User does not exist"}), 404

    # Check if the provided password matches the stored one
    if not check_password_hash(existing_user.password, password):
        return jsonify({"message": "Incorrect password"}), 401

    # If validation passes, return success response
    return jsonify({"message": "User validated successfully", "success": True,"user": {"email": existing_user.username, "occupation": existing_user.occupation}}), 200


@main.route('/createUser', methods=['POST'])
def create_user():
    try:
        user_data = request.get_json()  # Obtener el objeto JSON de la solicitud

        # Verificar si se recibieron los datos esperados
        if 'email' in user_data and 'password' in user_data:
            email = user_data['email']
            password = user_data['password']

            # Realizar alguna lógica con los datos recibidos
            # Por ejemplo, guardar el usuario en una base de datos
            user = User(email=email, password=password)
            db.session.add(user)
            db.session.commit()

            # Devolver una respuesta JSON
            response = {'message': 'Usuario creado exitosamente', 'email': email, 'password': password}
            return jsonify(response), 201  # 201 significa "Created"
        else:
            return jsonify({'error': 'Los datos del usuario son inválidos'}), 400  # 400 significa "Bad Request"

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # 500 significa "Internal Server Error"

