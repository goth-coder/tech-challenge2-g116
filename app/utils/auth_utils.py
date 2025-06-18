# This file has been moved to app/auth/auth_utils.py. Please use the new location.

import jwt
from datetime import datetime, timedelta, timezone
from flask import request, jsonify
from functools import wraps
from app.core.config import JWT_SECRET

def generate_token(user_id: int, role: str = "user") -> str:

    payload = {
        "user_id": user_id,
        "role": role,
        "exp": (datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            else:
                token = auth_header  # Accept just the token as well

        if not token:
            return jsonify({"error": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user_id = data["user_id"]  # Armazena o user_id pra uso na rota se quiser
            request.user_role = data.get("role", "user")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401

        return f(*args, **kwargs)
    return decorated
