import re


def normalize_skill_text(text):

    if not text:
        return ""

    text = text.lower()

    # Treat "dataanalytics" and "data analytics" as the same
    text = text.replace("dataanalytics", "data analytics")

    return text


def extract_skills(resume_text, skills_list):

    if not resume_text:
        return []

    text = normalize_skill_text(resume_text)

    found_skills = []

    for skill in skills_list:

        skill_lower = normalize_skill_text(skill)

        pattern = r"\b" + re.escape(skill_lower) + r"\b"

        if re.search(pattern, text):

            found_skills.append(skill)

    return found_skills


def get_skills_from_database(connection):

    cursor = connection.cursor()

    query = """
    SELECT id, skill_name, category
    FROM skills
    ORDER BY skill_name
    """

    cursor.execute(query)

    skills = cursor.fetchall()

    cursor.close()

    return skills