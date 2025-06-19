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

from app.auth.auth_utils import token_required

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/api/dashboard", methods=["GET"])
@swag_from(
    {
        "tags": ["Dashboard"],
        "security": [{"BearerAuth": []}],
        "responses": {
            200: {
                "description": "Access granted with valid JWT token",
                "examples": {
                    "application/json": {"message": "Welcome user 1 with role user!"}
                },
            },
            401: {"description": "Unauthorized - Invalid or missing token"},
        },
    }
)
@token_required
def dashboard_page():
    user_id = request.user_id
    user_role = request.user_role
    return jsonify({"message": f"Welcome user {user_id} with role {user_role}!"})


@user_routes.route("/dashboard", methods=["GET"])
def frontend_dashboard():
    # if not session.get("user_id"):
    #     print("User not logged in, redirecting to login page")
    #     return redirect(url_for("auth_routes.frontend_login"))
    return render_template("dashboard.html")
