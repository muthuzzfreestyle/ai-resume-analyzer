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
        "machine learning artificial intelligence":
            "machine learning",
        "deep learning artificial intelligence":
            "deep learning",
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

    return aliases.get(
        skill,
        skill
    )


def calculate_job_match(
    resume_skills,
    required_skills
):

    resume_set = {
        normalize_skill(skill)
        for skill in resume_skills
        if skill
    }

    required_set = {
        normalize_skill(skill)
        for skill in required_skills
        if skill
    }

    matched_skills = (
        resume_set.intersection(
            required_set
        )
    )

    missing_skills = (
        required_set - resume_set
    )

    if not required_set:

        match_score = 0.0

    else:

        match_score = (
            len(matched_skills)
            / len(required_set)
        ) * 100


    return {
        "match_score": round(
            match_score,
            2
        ),

        "matched_skills": sorted(
            matched_skills
        ),

        "missing_skills": sorted(
            missing_skills
        )
    }