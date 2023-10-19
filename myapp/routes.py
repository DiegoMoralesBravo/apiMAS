from flask import Blueprint, redirect, url_for, request, jsonify
from .extensions import db
from .models import User

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
    print(data)
    email = data.get('email')
    occupation = data.get('occupation')
    password = data.get('password')
    confirmPassword = data.get('confirmPassword')

    # Check if passwords match
    if password != confirmPassword:
        return jsonify({"message": "Passwords do not match"}), 400

    # If validation passes, add the user to the database
    user = User(username=email, password=password, occupation=occupation)
    db.session.add(user)
    db.session.commit()

    # Return success response
    return jsonify({"message": "User added successfully"}), 201
