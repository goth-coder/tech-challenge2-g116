import os

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
from flask_jwt_extended import JWTManager

from app.api.auth_routes import auth_routes
from app.api.user_routes import user_routes


class AppFactory:
    """
    Factory class for creating and configuring the Flask application
    with Swagger documentation, JWT authentication, and route blueprints.
    """

    def __init__(self):
        load_dotenv()  # Carrega as variáveis do arquivo .env
        self.app = Flask(__name__)
        self._configure_jwt()
        self._configure_swagger()
        self._register_blueprints()

    def _configure_jwt(self):
        """
        Configures JWT for the Flask app using flask-jwt-extended.
        """
        self.app.config["JWT_SECRET_KEY"] = os.getenv(
            "JWT_SECRET", "default-secret-key"
        )
        JWTManager(self.app)

    def _configure_swagger(self):
        """
        Configures Swagger UI using Flasgger.
        """
        swagger_config = {
            "headers": [],
            "specs": [
                {
                    "endpoint": "apispec",
                    "route": "/apispec.json",
                }
            ],
            "static_url_path": "/flasgger_static",
            "swagger_ui": True,
            "specs_route": "/apidocs/",
            "securityDefinitions": {
                "BearerAuth": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "Paste your JWT token here. Format: Bearer <token>",
                }
            },
        }
        Swagger(self.app, config=swagger_config)

    def _register_blueprints(self):
        """
        Registers route blueprints (like auth and user routes) with the Flask app.
        """
        self.app.register_blueprint(auth_routes)
        self.app.register_blueprint(user_routes)

    def get_app(self):
        return self.app


# --- App execution ---
app = AppFactory().get_app()


if __name__ == "__main__":
    app.run(debug=True)
