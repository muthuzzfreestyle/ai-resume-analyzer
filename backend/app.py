from flask import Flask, jsonify
from flask_cors import CORS
import hashlib
from config import Config, get_db_connection
from routes.auth_routes import auth_bp
from routes.resume_routes import resume_bp
from routes.history_routes import history_bp


app = Flask(__name__)

app.config.from_object(Config)

CORS(app)


# =========================
# REGISTER ROUTES
# =========================

app.register_blueprint(auth_bp)

app.register_blueprint(resume_bp)

app.register_blueprint(history_bp)


# =========================
# HOME
# =========================

@app.route("/")
def home():

    return jsonify({
        "status": "success",
        "message": "AI Resume Analyzer Backend is Running!"
    })


# =========================
# API STATUS
# =========================

@app.route("/api/status")
def status():

    try:

        connection = get_db_connection()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT DATABASE() AS database_name"
        )

        result = cursor.fetchone()

        cursor.close()

        connection.close()

        return jsonify({
            "status": "success",
            "message": "Backend connected to MySQL successfully!",
            "database": result["database_name"]
        }), 200

    except Exception as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


# =========================
# ERROR HANDLER
# =========================

@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "status": "error",
        "message": "API endpoint not found."
    }), 404


@app.errorhandler(500)
def server_error(error):

    return jsonify({
        "status": "error",
        "message": "Internal server error."
    }), 500


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )