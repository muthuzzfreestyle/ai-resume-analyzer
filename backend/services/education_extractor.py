import re


EDUCATION_PATTERNS = [
    r"\bbachelor of engineering\b",
    r"\bbachelor of technology\b",
    r"\bmaster of engineering\b",
    r"\bmaster of technology\b",
    r"\bbachelor of science\b",
    r"\bmaster of science\b",
    r"\bbachelor of computer applications\b",
    r"\bmaster of computer applications\b",
    r"\bbachelor of business administration\b",
    r"\bmaster of business administration\b",

    r"\bb\.?\s*e\.?\b",
    r"\bb\.?\s*tech\.?\b",
    r"\bm\.?\s*e\.?\b",
    r"\bm\.?\s*tech\.?\b",
    r"\bb\.?\s*sc\.?\b",
    r"\bm\.?\s*sc\.?\b",
    r"\bbca\b",
    r"\bmca\b",
    r"\bmba\b",

    r"\bbachelor\b",
    r"\bmaster\b",
    r"\bdiploma\b",

    r"\bcomputer science and engineering\b",
    r"\bcomputer science\b",
    r"\binformation technology\b",
    r"\belectronics and communication engineering\b",
    r"\belectrical and electronics engineering\b",
    r"\bmechanical engineering\b",
    r"\bcivil engineering\b",
    r"\bengineering\b"
]


def extract_education(resume_text):

    if not resume_text:
        return []

    text = resume_text.lower()

    # Normalize common separators
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    found_education = []

    for pattern in EDUCATION_PATTERNS:

        matches = re.findall(pattern, text)

        for match in matches:

            value = match.strip()

            if value and value not in found_education:
                found_education.append(value)

    return found_education