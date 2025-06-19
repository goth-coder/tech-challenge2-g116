import jwt
from flasgger import swag_from
from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from pydantic import ValidationError

from app.auth.auth_service import AuthService
from app.core.config import JWT_SECRET
from app.models.models import LoginSchema, SignupSchema

auth_routes = Blueprint("auth_routes", __name__)


def format_pydantic_errors(errors):
    formatted = []
    for error in errors:
        field = ".".join(str(loc) for loc in error["loc"])
        msg = error["msg"]
        formatted.append(f"- Campo '{field}': {msg}")
    return "Erro de validação nos dados enviados:\n\n" + "\n".join(formatted)


def format_validation_errors(errors):
    messages = []
    for err in errors:
        loc = ".".join(str(l) for l in err.get("loc", []))
        msg = err.get("msg", "Erro de validação")
        messages.append(f"Campo '{loc}': {msg}")
    return messages


@auth_routes.route("/login", methods=["POST"])
@swag_from(
    {
        "tags": ["Auth"],
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string"},
                        "password": {"type": "string"},
                    },
                    "required": ["email", "password"],
                },
            }
        ],
        "responses": {
            200: {"description": "Login successful"},
            401: {"description": "Invalid credentials"},
            404: {"description": "User not found"},
            400: {"description": "Validation error"},
        },
    }
)
def login_user():
    try:
        data = request.get_json()
        login_data = LoginSchema(**data)
        result, status = AuthService.login(login_data.email, login_data.password)
        # If login is successful, set session["user_id"]
        if status == 200 and "token" in result:
            token = result["token"]
            try:
                payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
                session["user_id"] = payload["user_id"]
            except Exception: 
                pass
        return jsonify(result), status
    except ValidationError as e:
        return jsonify(
            {
                "error": f"Erro de validação nos dados enviados: {format_validation_errors(e.errors())}",
            }
        ), 400


@auth_routes.route("/signup", methods=["POST"])
@swag_from(
    {
        "tags": ["Auth"],
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "username": {"type": "string"},
                        "email": {"type": "string"},
                        "age": {"type": "integer"},
                        "password": {"type": "string"},
                    },
                    "required": ["name", "username", "email", "password"],
                },
            }
        ],
        "responses": {
            201: {"description": "User registered successfully"},
            400: {"description": "Bad request"},
        },
    }
)
def signup_user():
    try:
        data = SignupSchema.model_validate(request.get_json())
    except ValidationError as e:
        formatted_error = format_pydantic_errors(e.errors())
        return jsonify({"error": formatted_error}), 400

    response, status = AuthService.signup(
        data.name, data.username, data.email, data.age, data.password
    )
    return jsonify(response), status


@auth_routes.route("/logout")
def logout():
    session.clear()  # Destroi todos os dados da sessão
    return redirect(url_for("auth_routes.frontend_login"))


# This route is for rendering the frontend login page
@auth_routes.route("/login", methods=["GET"])
def frontend_login():
    if session.get("user_id"):
        return redirect(url_for("user_routes.dashboard"))
    return render_template("login.html")


# This route is for rendering the frontend signup page
@auth_routes.route("/signup", methods=["GET"])
def frontend_signup():
    if session.get("user_id"):
        return redirect(url_for("user_routes.dashboard"))
    return render_template("signup.html")
