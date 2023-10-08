from flask import Blueprint, redirect, url_for, request, jsonify
from .extensions import db
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    users = User.query.all()
    users_list_html = [f"<li>{ user.email }</li>" for user in users]
    return f"<ul>{''.join(users_list_html)}</ul>"

@main.route('/add/<username>')
def add_user(username):
    db.session.add(User(username=username, password='test'))
    db.session.commit()
    return redirect(url_for("main.index"))

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
