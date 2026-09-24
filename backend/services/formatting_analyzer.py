import re


REQUIRED_SECTIONS = {
    "contact": [
        "email",
        "phone",
        "mobile",
        "linkedin"
    ],
    "summary": [
        "summary",
        "profile",
        "objective"
    ],
    "education": [
        "education",
        "academic",
        "qualification"
    ],
    "skills": [
        "skills",
        "technical skills",
        "technical skill"
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "internship"
    ],
    "projects": [
        "project",
        "projects"
    ]
}


def analyze_formatting(resume_text):

    if not resume_text:
        return 0.0

    text = resume_text.lower()

    section_score = 0

    # =========================
    # REQUIRED SECTION CHECK
    # =========================

    for keywords in REQUIRED_SECTIONS.values():

        found = False

        for keyword in keywords:

            pattern = (
                r"\b"
                + re.escape(keyword)
                + r"\b"
            )

            if re.search(pattern, text):

                found = True
                break

        if found:
            section_score += 10


    # =========================
    # TEXT LENGTH CHECK
    # =========================

    word_count = len(
        text.split()
    )

    if word_count >= 150:
        section_score += 10


    # =========================
    # EMAIL CHECK
    # =========================

    email_pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}"
    )

    if re.search(
        email_pattern,
        text
    ):

        section_score += 10


    # =========================
    # PHONE CHECK
    # =========================

    phone_patterns = [
        r"\b\d{10}\b",
        r"\+\d{1,3}[\s-]?\d{10}\b",
        r"\b\d{5}[\s-]\d{5}\b"
    ]

    phone_found = False

    for pattern in phone_patterns:

        if re.search(
            pattern,
            text
        ):

            phone_found = True
            break


    if phone_found:
        section_score += 10


    # =========================
    # LIMIT SCORE
    # =========================

    return float(
        min(
            section_score,
            100
        )
    )