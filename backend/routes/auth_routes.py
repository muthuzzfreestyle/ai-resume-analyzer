from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import get_db_connection
from models.user_model import UserModel


auth_bp = Blueprint("auth", __name__)


# =========================
# REGISTER
# =========================

@auth_bp.route("/api/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "status": "error",
            "message": "Name, email and password are required"
        }), 400

    connection = get_db_connection()

    try:

        user_model = UserModel(connection)

        existing_user = user_model.get_user_by_email(email)

        if existing_user:
            return jsonify({
                "status": "error",
                "message": "Email already registered"
            }), 409

        password_hash = generate_password_hash(password)

        user_id = user_model.create_user(
            name,
            email,
            password_hash
        )

        return jsonify({
            "status": "success",
            "message": "User registered successfully",
            "user_id": user_id
        }), 201

    finally:
        connection.close()


# =========================
# LOGIN
# =========================

@auth_bp.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "status": "error",
            "message": "Email and password are required"
        }), 400

    connection = get_db_connection()

    try:

        user_model = UserModel(connection)

        user = user_model.get_user_by_email(email)

        if not user:
            return jsonify({
                "status": "error",
                "message": "Invalid email or password"
            }), 401

        password_hash = user["password_hash"]

        if not check_password_hash(password_hash, password):
            return jsonify({
                "status": "error",
                "message": "Invalid email or password"
            }), 401

        return jsonify({
            "status": "success",
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            }
        }), 200

    finally:
        connection.close()