from flask import Blueprint, redirect, url_for, request, jsonify
from .extensions import db
from .models import User
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
    occupation = data['occupation']
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


@main.route('/generation', methods=['POST'])
def generation():
    # Get data from the request
    data = request.get_json()
    
    
    return jsonify({"message": "Test completed"}), 200
