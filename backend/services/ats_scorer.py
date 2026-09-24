def normalize_skill(skill):
    if not skill:
        return ""

    skill = skill.lower().strip()

    aliases = {
        "python programming": "python",
        "java programming": "java",
        "c programming": "c",
        "c++ programming": "c++",
        "javascript programming": "javascript",
        "html web development": "html",
        "css web development": "css",
        "sql database": "sql",
        "mysql database": "mysql",
        "mongodb database": "mongodb",
        "excel data analysis": "excel",
        "power bi data visualization": "power bi",
        "tableau data visualization": "tableau",
        "machine learning artificial intelligence": "machine learning",
        "deep learning artificial intelligence": "deep learning",
        "git tools": "git",
        "github tools": "github",
        "aws cloud": "aws",
        "azure cloud": "azure",
        "data analytics": "data analytics",
        "statistics": "statistics",
        "pandas": "pandas",
        "numpy": "numpy",
        "scikit-learn": "scikit-learn",
        "powerpoint": "powerpoint",
        "microsoft word": "microsoft word"
    }

    return aliases.get(skill, skill)


def calculate_skill_score(detected_skills, relevant_skills):

    if not relevant_skills:
        return 0.0

    detected = {
        normalize_skill(skill)
        for skill in detected_skills
        if skill
    }

    relevant = {
        normalize_skill(skill)
        for skill in relevant_skills
        if skill
    }

    matched = detected.intersection(relevant)

    return round(
        (len(matched) / len(relevant)) * 100,
        2
    )


def calculate_education_score(education):

    if not education:
        return 0.0

    return 100.0


def calculate_experience_score(experience):

    if not experience:
        return 0.0

    return 100.0


def calculate_ats_score(
    skill_score,
    education_score=0,
    experience_score=0,
    formatting_score=0
):

    score = (
        (skill_score * 0.40)
        + (education_score * 0.20)
        + (experience_score * 0.20)
        + (formatting_score * 0.20)
    )

    return round(min(score, 100), 2)