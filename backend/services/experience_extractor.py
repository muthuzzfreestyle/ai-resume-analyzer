import re


EXPERIENCE_PATTERNS = [
    r"\bwork experience\b",
    r"\bprofessional experience\b",
    r"\bcareer experience\b",
    r"\bemployment history\b",
    r"\bwork history\b",
    r"\bexperience\b",

    r"\binternship\b",
    r"\bintern\b",

    r"\bdata analyst\b",
    r"\bsoftware developer\b",
    r"\bsoftware engineer\b",
    r"\bweb developer\b",
    r"\bpython developer\b",
    r"\bjava developer\b",
    r"\bmachine learning engineer\b",
    r"\bdata scientist\b",
    r"\bdeveloper\b",
    r"\bengineer\b",

    r"\bproject experience\b",
    r"\bworked\b",
    r"\bworking\b",
    r"\bfreelance\b",
    r"\bfreelancer\b",
    r"\bfresher\b"
]


def extract_experience(resume_text):

    if not resume_text:
        return []

    text = resume_text.lower()

    # Normalize common separators
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    found_experience = []

    for pattern in EXPERIENCE_PATTERNS:

        matches = re.findall(pattern, text)

        for match in matches:

            value = match.strip()

            if value and value not in found_experience:
                found_experience.append(value)

    return found_experience