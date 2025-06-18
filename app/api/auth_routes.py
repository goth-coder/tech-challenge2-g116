from flask import Blueprint, request, jsonify
from flasgger import swag_from 
from app.auth.auth_service import AuthService
from pydantic import ValidationError
from app.models.models import LoginSchema, SignupSchema
auth_routes = Blueprint('auth_routes', __name__)


@auth_routes.route('/login', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        200: {'description': 'Login successful'},
        401: {'description': 'Invalid credentials'},
        404: {'description': 'User not found'}
    }
})
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400
    try:
        data = LoginSchema.parse_obj(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    response, status = AuthService.login(data.email, data.password)
    return jsonify(response), status


@auth_routes.route('/signup', methods=['POST'])
@swag_from({
    'tags': ['Auth'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'age': {'type': 'integer'},
                    'password': {'type': 'string'}
                },
                'required': ['name', 'username', 'email', 'password']
            }
        }
    ],
    'responses': {
        201: {'description': 'User registered successfully'},
        400: {'description': 'Bad request'}
    }
})
def signup_user():
    data = request.json
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    age = data.get('age')
    password = data.get('password')
    if not all([name, username, email, password]):
        return jsonify({"error": "Missing required fields"}), 400
    try:
        data = SignupSchema.parse_obj(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    response, status = AuthService.signup(data.name, data.username, data.email, data.age, data.password)
    return jsonify(response), status


