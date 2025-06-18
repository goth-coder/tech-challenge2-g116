from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.auth.auth_utils import token_required

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/protected', methods=['GET'])
@swag_from({
    'tags': ['Protected'],
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {
            'description': 'Access granted with valid JWT token',
            'examples': {
                'application/json': {
                    'message': 'Welcome user 1 with role user!'
                }
            }
        },
        401: {
            'description': 'Unauthorized - Invalid or missing token'
        }
    }
})
@token_required
def protected_route():
    user_id = request.user_id
    user_role = request.user_role
    return jsonify({"message": f"Welcome user {user_id} with role {user_role}!"})

