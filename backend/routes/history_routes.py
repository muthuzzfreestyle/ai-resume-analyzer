from flask import Blueprint, jsonify, send_file
from config import get_db_connection
import os


history_bp = Blueprint("history", __name__)


# =========================
# GET USER RESUME HISTORY
# =========================

@history_bp.route(
    "/api/user/<int:user_id>/resumes",
    methods=["GET"]
)
def get_resume_history(user_id):

    connection = get_db_connection()

    try:

        cursor = connection.cursor()

        query = """
        SELECT
            r.id,
            r.file_name,
            r.uploaded_at,
            a.ats_score,
            a.skill_score,
            a.education_score,
            a.experience_score,
            a.formatting_score
        FROM resumes r
        LEFT JOIN analyses a
            ON r.id = a.resume_id
        WHERE r.user_id = %s
        ORDER BY r.uploaded_at DESC
        """

        cursor.execute(query, (user_id,))

        resumes = cursor.fetchall()

        return jsonify({
            "status": "success",
            "resumes": resumes
        }), 200

    except Exception as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500

    finally:

        connection.close()


# =========================
# DOWNLOAD RESUME
# =========================

@history_bp.route(
    "/api/resume/<int:resume_id>/download",
    methods=["GET"]
)
def download_resume(resume_id):

    connection = get_db_connection()

    try:

        cursor = connection.cursor()

        query = """
        SELECT
            file_name,
            file_path
        FROM resumes
        WHERE id = %s
        """

        cursor.execute(query, (resume_id,))

        resume = cursor.fetchone()

        if not resume:

            return jsonify({
                "status": "error",
                "message": "Resume not found."
            }), 404

        file_path = resume["file_path"]

        if not os.path.exists(file_path):

            return jsonify({
                "status": "error",
                "message": "Resume file not found."
            }), 404

        return send_file(
            file_path,
            as_attachment=True,
            download_name=resume["file_name"]
        )

    except Exception as error:

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500

    finally:

        connection.close()


# =========================
# DELETE RESUME
# =========================

@history_bp.route(
    "/api/resume/<int:resume_id>",
    methods=["DELETE"]
)
def delete_resume(resume_id):

    connection = get_db_connection()

    try:

        cursor = connection.cursor()

        query = """
        SELECT file_path
        FROM resumes
        WHERE id = %s
        """

        cursor.execute(query, (resume_id,))

        resume = cursor.fetchone()

        if not resume:

            return jsonify({
                "status": "error",
                "message": "Resume not found."
            }), 404

        file_path = resume["file_path"]

        delete_query = """
        DELETE FROM resumes
        WHERE id = %s
        """

        cursor.execute(
            delete_query,
            (resume_id,)
        )

        connection.commit()

        if file_path and os.path.exists(file_path):

            os.remove(file_path)

        return jsonify({
            "status": "success",
            "message": "Resume deleted successfully."
        }), 200

    except Exception as error:

        connection.rollback()

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500

    finally:

        connection.close()