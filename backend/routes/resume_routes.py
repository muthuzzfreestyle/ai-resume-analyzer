from flask import Blueprint, request, jsonify
import os

from config import get_db_connection
from services.resume_parser import extract_resume_text
from services.text_cleaner import clean_text
from services.skill_extractor import (
    extract_skills,
    get_skills_from_database
)
from services.education_extractor import extract_education
from services.experience_extractor import extract_experience
from services.formatting_analyzer import analyze_formatting
from services.ats_scorer import (
    calculate_skill_score,
    calculate_education_score,
    calculate_experience_score,
    calculate_ats_score
)
from services.job_matcher import calculate_job_match


resume_bp = Blueprint("resume", __name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================
# UPLOAD RESUME
# =========================

@resume_bp.route("/api/upload-resume", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No resume file uploaded."
        }), 400

    file = request.files["resume"]

    if not file.filename:
        return jsonify({
            "status": "error",
            "message": "No file selected."
        }), 400

    user_id = request.form.get("user_id")

    if not user_id:
        return jsonify({
            "status": "error",
            "message": "User ID is required."
        }), 400

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in [".pdf", ".docx"]:
        return jsonify({
            "status": "error",
            "message": "Only PDF and DOCX files are supported."
        }), 400

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(file_path)

    connection = get_db_connection()

    try:

        extracted_text = extract_resume_text(file_path)

        cleaned_text = clean_text(extracted_text)

        cursor = connection.cursor()

        query = """
        INSERT INTO resumes
        (
            user_id,
            file_name,
            file_path,
            extracted_text,
            cleaned_text
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                user_id,
                file.filename,
                file_path,
                extracted_text,
                cleaned_text
            )
        )

        connection.commit()

        resume_id = cursor.lastrowid

        cursor.close()

        return jsonify({
            "status": "success",
            "message": "Resume uploaded successfully.",
            "resume_id": resume_id
        }), 201

    except Exception as error:

        connection.rollback()

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500

    finally:

        connection.close()


# =========================
# ANALYZE RESUME
# =========================

@resume_bp.route(
    "/api/resume/<int:resume_id>/analyze",
    methods=["GET", "POST"]
)
def analyze_resume(resume_id):

    connection = get_db_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM resumes
            WHERE id = %s
            """,
            (resume_id,)
        )

        resume = cursor.fetchone()

        if not resume:

            return jsonify({
                "status": "error",
                "message": "Resume not found."
            }), 404

        resume_text = resume.get("cleaned_text")

        if not resume_text:
            resume_text = clean_text(
                resume.get("extracted_text", "")
            )

        # =========================
        # SKILLS
        # =========================

        skills_from_db = get_skills_from_database(
            connection
        )

        skill_names = [
            skill["skill_name"]
            for skill in skills_from_db
        ]

        detected_skills = extract_skills(
            resume_text,
            skill_names
        )

        # =========================
        # EDUCATION
        # =========================

        education = extract_education(
            resume_text
        )

        # =========================
        # EXPERIENCE
        # =========================

        experience = extract_experience(
            resume_text
        )

        # =========================
        # SCORES
        # =========================

        skill_score = calculate_skill_score(
            detected_skills,
            skill_names
        )

        education_score = calculate_education_score(
            education
        )

        experience_score = calculate_experience_score(
            experience
        )

        formatting_score = analyze_formatting(
            resume_text
        )

        ats_score = calculate_ats_score(
            skill_score,
            education_score,
            experience_score,
            formatting_score
        )

        # =========================
        # SAVE RESUME SKILLS
        # =========================

        cursor.execute(
            """
            DELETE FROM resume_skills
            WHERE resume_id = %s
            """,
            (resume_id,)
        )

        for skill in skills_from_db:

            if skill["skill_name"] in detected_skills:

                cursor.execute(
                    """
                    INSERT IGNORE INTO resume_skills
                    (
                        resume_id,
                        skill_id,
                        confidence
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        resume_id,
                        skill["id"],
                        100.00
                    )
                )

        # =========================
        # SUGGESTIONS
        # =========================

        suggestions = []

        if skill_score < 70:
            suggestions.append(
                "Add more relevant technical skills."
            )

        if education_score == 0:
            suggestions.append(
                "Add your education details."
            )

        if experience_score == 0:
            suggestions.append(
                "Add your work experience or internship details."
            )

        if formatting_score < 70:
            suggestions.append(
                "Improve resume formatting and add important sections."
            )

        if not suggestions:
            suggestions.append(
                "Your resume contains the main required sections."
            )

        summary = (
            f"Resume analysis completed with an ATS score "
            f"of {ats_score}%."
        )

        suggestions_text = "\n".join(
            f"- {suggestion}"
            for suggestion in suggestions
        )

        # =========================
        # SAVE ANALYSIS
        # =========================

        cursor.execute(
            """
            DELETE FROM analyses
            WHERE resume_id = %s
            """,
            (resume_id,)
        )

        cursor.execute(
            """
            INSERT INTO analyses
            (
                resume_id,
                ats_score,
                skill_score,
                education_score,
                experience_score,
                formatting_score,
                summary,
                suggestions
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                resume_id,
                ats_score,
                skill_score,
                education_score,
                experience_score,
                formatting_score,
                summary,
                suggestions_text
            )
        )

        connection.commit()

        return jsonify({
            "status": "success",
            "message": "Resume analyzed successfully.",
            "resume_id": resume_id,
            "ats_score": ats_score,
            "skill_score": skill_score,
            "education_score": education_score,
            "experience_score": experience_score,
            "formatting_score": formatting_score,
            "detected_skills": detected_skills,
            "education": education,
            "experience": experience,
            "summary": summary,
            "suggestions": suggestions
        }), 200

    except Exception as error:

        connection.rollback()

        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500

    finally:

        connection.close()


# =========================
# GET RESUME SKILLS
# =========================

@resume_bp.route(
    "/api/resume/<int:resume_id>/skills",
    methods=["GET"]
)
def get_resume_skills(resume_id):

    connection = get_db_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                skills.id,
                skills.skill_name,
                skills.category,
                resume_skills.confidence
            FROM resume_skills
            JOIN skills
                ON resume_skills.skill_id = skills.id
            WHERE resume_skills.resume_id = %s
            ORDER BY skills.skill_name
            """,
            (resume_id,)
        )

        skills = cursor.fetchall()

        return jsonify({
            "status": "success",
            "resume_id": resume_id,
            "skills": skills
        }), 200

    finally:

        connection.close()


# =========================
# GET ANALYSIS
# =========================

@resume_bp.route(
    "/api/resume/<int:resume_id>/analysis",
    methods=["GET"]
)
def get_analysis(resume_id):

    connection = get_db_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM analyses
            WHERE resume_id = %s
            ORDER BY analyzed_at DESC
            LIMIT 1
            """,
            (resume_id,)
        )

        analysis = cursor.fetchone()

        if not analysis:

            return jsonify({
                "status": "error",
                "message": "Analysis not found."
            }), 404

        return jsonify({
            "status": "success",
            "analysis": analysis
        }), 200

    finally:

        connection.close()


# =========================
# GET JOBS
# =========================

@resume_bp.route(
    "/api/jobs",
    methods=["GET"]
)
def get_jobs():

    connection = get_db_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM jobs
            ORDER BY created_at DESC
            """
        )

        jobs = cursor.fetchall()

        return jsonify({
            "status": "success",
            "jobs": jobs
        }), 200

    finally:

        connection.close()


# =========================
# MATCH RESUME WITH JOB
# =========================

@resume_bp.route(
    "/api/resume/<int:resume_id>/jobs/<int:job_id>/match",
    methods=["GET"]
)
def match_resume_job(resume_id, job_id):

    connection = get_db_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT skill_name
            FROM skills
            JOIN resume_skills
                ON skills.id = resume_skills.skill_id
            WHERE resume_skills.resume_id = %s
            """,
            (resume_id,)
        )

        resume_skill_rows = cursor.fetchall()

        resume_skills = [
            row["skill_name"]
            for row in resume_skill_rows
        ]

        cursor.execute(
            """
            SELECT *
            FROM jobs
            WHERE id = %s
            """,
            (job_id,)
        )

        job = cursor.fetchone()

        if not job:

            return jsonify({
                "status": "error",
                "message": "Job not found."
            }), 404

        required_skills = [
            skill.strip()
            for skill in job["required_skills"].split(",")
            if skill.strip()
        ]

        result = calculate_job_match(
            resume_skills,
            required_skills
        )

        cursor.execute(
            """
            INSERT INTO job_matches
            (
                resume_id,
                job_id,
                match_score,
                matched_skills,
                missing_skills
            )
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                match_score = VALUES(match_score),
                matched_skills = VALUES(matched_skills),
                missing_skills = VALUES(missing_skills)
            """,
            (
                resume_id,
                job_id,
                result["match_score"],
                ", ".join(result["matched_skills"]),
                ", ".join(result["missing_skills"])
            )
        )

        connection.commit()

        return jsonify({
            "status": "success",
            "resume_id": resume_id,
            "job": job,
            "match_score": result["match_score"],
            "matched_skills": result["matched_skills"],
            "missing_skills": result["missing_skills"]
        }), 200

    finally:

        connection.close()