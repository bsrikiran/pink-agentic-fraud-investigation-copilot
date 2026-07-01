"""
Purpose: Sharing formatting helpers and tracking structured chunk configurations.
"""
import re

def clean_text_whitespace(text: str) -> str:
    """Removes irregular newlines, excessive spacing, and page-break artifacts."""
    if not text:
        return ""
    # Replace multiple spaces/newlines with a single space
    cleaned = re.sub(re.compile(r'\s+'), ' ', text)
    return cleaned.strip()

def extract_policy_identifiers(filename: str) -> tuple[str, str]:
    """
    Parses structural file string names to extract document titles and codes.
    Example: 'Fraud Investigation Policy (FP-214).pdf' -> ('Fraud Investigation Policy', 'FP-214')

    Files without an explicit '(code)' in their name (e.g. 'fraud_policy.pdf') get a
    readable title-cased name, and the identifier falls back to the file's own slug
    (e.g. 'fraud_policy') rather than a shared generic placeholder or an invented code.
    """
    clean_name = filename.replace(".pdf", "")
    match = re.search(re.compile(r'\((.*?)\)'), clean_name)

    if match:
        policy_id = match.group(1)
        policy_name = clean_name.split("(")[0].strip()
        return policy_name, policy_id

    words = [w for w in re.split(r'[_\-\s]+', clean_name) if w]
    policy_name = " ".join(w.capitalize() for w in words)
    return policy_name, clean_name
