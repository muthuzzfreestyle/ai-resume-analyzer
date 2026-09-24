import re


def clean_text(text):

    if not text:
        return ""

    # Convert to lowercase
    text = text.lower()

    # Replace multiple spaces and new lines
    text = re.sub(r"\s+", " ", text)

    # Remove unwanted special characters
    text = re.sub(r"[^a-z0-9\s.,+#-]", "", text)

    # Remove extra spaces
    text = text.strip()

    return text